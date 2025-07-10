package test

import (
	"gql-cost-profiler/analyzer"
	"testing"
)



func TestExtractNodes(t *testing.T) {
	var testSchema = `
			schema {
			query: Query
			}

			type Query {
			user(id: ID!): User
			posts(first: Int): [Post]
			}

			type User {
			id: ID!
			name: String!
			email: String
			posts(limit: Int): [Post]
			}

			type Post {
			id: ID!
			title: String!
			content: String
			author: User
			}`
	var testQuery = `
		query TestUserAndPosts {
		user(id: "1") {
			id
			name
			... on User {
			email
			}
			posts(limit: 5) {
			...PostFields
			}
		}
		posts(first: 10) {
			...PostFields
		}
		}

		fragment PostFields on Post {
		id
		title
		content
		author {
			id
			name
		}
		}
		`

	schema,err := analyzer.ParseGQLSchema(testSchema)
	if err != nil {
		t.Errorf("error %s", err)
		return
	}
	doc,err := analyzer.ParseGQLQuery(schema,testQuery)
	if err != nil {
		t.Errorf("error %s", err)
		return
	}
	extractedNodes := analyzer.ExtractQueryNodes(doc, schema)

	for parentType,nodes := range extractedNodes {
		t.Logf("Type: %s\n", parentType)

		for _,node := range nodes {
			t.Logf("Field type: %s\n", node.FieldName)

			for _,arg := range node.FieldArguments {
				t.Logf("      - %s: %v\n", arg.Name, arg.Value)
			}
		}
	}

}
