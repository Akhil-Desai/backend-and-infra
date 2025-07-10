package analyzer

import (
	"fmt"
	"strconv"

	"github.com/vektah/gqlparser/v2"
	"github.com/vektah/gqlparser/v2/ast"
	"github.com/vektah/gqlparser/v2/validator"
)


type Node struct {
	FieldName string
	FieldArguments   []*FieldArgument
}
type FieldArgument struct {
	Name string
	Value interface{}
}


func ParseGQLSchema(schemaStr string) (*ast.Schema, error) {
	schema,err := gqlparser.LoadSchema(&ast.Source{Name: "schema.graphql", Input: schemaStr})
	if err != nil {
		return nil, fmt.Errorf("failed to parse schmea: %w 💥", err)
	}
	return schema, nil
}

func ParseGQLQuery(schema *ast.Schema, queryStr string) (*ast.QueryDocument, error) {
	query, err := gqlparser.LoadQuery(schema, queryStr)
	if err != nil {
		return nil, fmt.Errorf("failed to parse query: %w 💥", err)
	}
	errs := validator.Validate(schema, query)
	if len(errs) > 0 {
		return nil, fmt.Errorf("query validaton errors: %v 💥", errs)
	}
	return query, nil
}

func ExtractQueryNodes(doc *ast.QueryDocument, schema *ast.Schema)(map[string][]*Node) {
	// Returns a Map Structured like
	// { P_Type: *Node{
	// 			field name,
	// 			field arguments
	//		}
	// }
	nodes := make(map[string][]*Node)
	visitedFragments := make(map[string]struct{})


	var walkSelections func(selections ast.SelectionSet, parentType string)
	walkSelections = func(selections ast.SelectionSet, parentType string) {

		for _,sel := range selections{
			switch s := sel.(type){

			case *ast.Field:

				fieldDef := schema.Types[parentType].Fields.ForName(s.Name)
				if fieldDef == nil {
					continue
				}

				var newFieldArgs []*FieldArgument
				for _,arg := range s.Arguments {
					newFieldArgs = append(newFieldArgs,
						&FieldArgument{
						Name: arg.Name,
						Value : arg.Value.Raw,
					})
				}
				nodes[parentType] = append(nodes[parentType], &Node{FieldName: s.Name, FieldArguments: newFieldArgs})

				walkSelections(s.SelectionSet, fieldDef.Type.Name())

			case *ast.FragmentSpread:

				if _, ok := visitedFragments[s.Name]; ok {
					continue
				}
				visitedFragments[s.Name] = struct{}{}
				frag := doc.Fragments.ForName(s.Name)
				if frag != nil {
					walkSelections(frag.SelectionSet, frag.TypeCondition)
				}
			case *ast.InlineFragment:
				walkSelections(s.SelectionSet, s.TypeCondition )
			}
		}
	}

	for _,op := range doc.Operations {
		var rootType string
		switch op.Operation {
		case ast.Query:
			rootType = "Query"
		case ast.Mutation:
			rootType = "Mutation"
		case ast.Subscription:
			rootType = "Subscription"

		}

		walkSelections(op.SelectionSet, rootType)
	}

	return nodes
}

func applyCost(nodes map[string][]*Node, config map[string]map[string]map[string]interface{}) (float64,error) {

	cost := float64(0)

	for parentType,nodes := range nodes {

		for _,node := range nodes {

			fieldCfg,ok := config[parentType][node.FieldName]
			if !ok { continue }

			baseCost,err := convertToFloat64(fieldCfg["base"])
			if err != nil { return float64(-1) ,fmt.Errorf("%w", err) }
			cost = baseCost + cost

			perItemArg,hasArg := fieldCfg["perItemArg"].(string)
			if !hasArg { continue }

			perItemCost,err := convertToFloat64(fieldCfg["perItemCost"])
			if err != nil { return float64(-1) ,fmt.Errorf("%w", err) }

			for _,arg := range node.FieldArguments {

				if arg.Name == perItemArg {

					argVal,err := convertToFloat64(arg.Value)
					if err != nil { return float64(-1) ,fmt.Errorf("%w", err) }
					cost = (argVal * perItemCost) + cost

				}

			}

		}

	}
	return cost,nil
}

func convertToFloat64(value interface{}) (float64,error){

	switch t := value.(type){
	case string:
		newValue, err := strconv.ParseFloat(t, 64)
		if err != nil {
			return float64(-1) , fmt.Errorf("error converting type string to float64 for value... %w 💥", err)
		}
		return newValue,nil

	case int:
		newValue := float64(value.(int))
		return newValue,nil

	case float64:
		return value.(float64),nil

	default:
		return float64(-1) , fmt.Errorf("invalid type for converting to float64 for perItemCost... type was: %T 💥", t)
	}
}
