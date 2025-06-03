package analyzer

import (
	"fmt"
	"github.com/vektah/gqlparser/v2"
	"github.com/vektah/gqlparser/v2/ast"
	"github.com/vektah/gqlparser/v2/validator"
)

type Argument struct {
		Name string
		Value interface{}
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

func ExtractQueryNodes(doc *ast.QueryDocument)(map[string][]Argument) {
	//For Each SelectionSet we encounter a Field which can contain another Field FragmentSpread and Inline Fragment
	//We can then recurse on each Field,Fragment,and InlineFragment extracting the Variable and any Arguments used with that Variable
	used := make(map[string][]Argument)
	visitedFragments := make(map[string]struct{})


	var walkSelections func(selections ast.SelectionSet)
	walkSelections = func(selections ast.SelectionSet) {

		for _,sel := range selections{
			switch s := sel.(type){
			case *ast.Field:

				for _,arg := range s.Arguments {
					if arg.Value.Kind == ast.Variable {
						used[s.Name] = append(used[s.Name], Argument{Name: arg.Name, Value: ast.Variable})
					} else {
						used[s.Name] = append(used[s.Name], Argument{Name: arg.Name, Value: arg.Value.Raw})
					}
				}
				walkSelections(s.SelectionSet)
			case *ast.FragmentSpread:
				if _,exist := visitedFragments[s.Name]; exist {
					continue
				}
				visitedFragments[s.Name] = struct{}{}
				frag := doc.Fragments.ForName(s.Name)
				if frag != nil {
					walkSelections(frag.SelectionSet)
				}
			case *ast.InlineFragment:
				walkSelections(s.SelectionSet)
			}
		}
	}

	for _,operations := range doc.Operations {
		walkSelections(operations.SelectionSet)
	}

	return used
}
