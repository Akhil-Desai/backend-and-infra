package analyzer

import (
	"fmt"
	"github.com/vektah/gqlparser/v2"
	"github.com/vektah/gqlparser/v2/ast"
	"github.com/vektah/gqlparser/v2/validator"
)

//We want our extracted nodes to be like Parent -> Field Name -> Arguments
type QLNode struct {
	f_name string
	args   []*Argument
}

type Argument struct {
	name string
	isVar bool
	val interface{} //nil or int
}


func ParseGQLSchema(schemaStr string) (*ast.Schema, error) {
	schema,err := gqlparser.LoadSchema(&ast.Source{Name: "schema.graphql", Input: schemaStr})
	if err != nil {
		return nil, fmt.Errorf("failed to parse schmea: %w", err)
	}
	return schema, nil
}

func ParseGQLQuery(schema *ast.Schema, queryStr string) (*ast.QueryDocument, error) {
	query, err := gqlparser.LoadQuery(schema, queryStr)
	if err != nil {
		return nil, fmt.Errorf("failed to parse query: %w", err)
	}
	errs := validator.Validate(schema, query)
	if len(errs) > 0 {
		return nil, fmt.Errorf("query validaton errors: %v", errs)
	}
	return query, nil
}

func ExtractQueryNodes(doc *ast.QueryDocument, schema *ast.Schema)(map[string][]QLNode) {
	//For Each SelectionSet we encounter a Field which can contain another Field FragmentSpread and Inline Fragment
	//We can then recurse on each Field,Fragment,and InlineFragment extracting the Variable and any Arguments used with that Variable
	nodes := make(map[string][]*QLNode)
	visitedFragments := make(map[string]struct{})


	var walkSelections func(selections ast.SelectionSet, p_type string)
	walkSelections = func(selections ast.SelectionSet, p_type string) {

		for _,sel := range selections{
			switch s := sel.(type){

			case *ast.Field:
				//Extract the parent type
				fieldDef := schema.Types[p_type].Fields.ForName(s.Name)
				if fieldDef == nil {
					continue
				}
				var newArgs []*Argument
				for _,a := range s.Arguments {
					newArgs = append(newArgs,
						&Argument{
						name: a.Name,
						isVar: a.Value.Kind == ast.Variable,
						val : a.Value.Raw,
					})
				}
				nodes[p_type] = append(nodes[p_type], &QLNode{f_name: s.Name, args: newArgs})

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

		walkSelections(op.SelectionSet, rootType)
		}
	}

	return nodes
}
