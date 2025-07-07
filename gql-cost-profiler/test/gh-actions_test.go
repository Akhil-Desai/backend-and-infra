package test

import (
	"testing"
)

func TestActions(t *testing.T) {
	helloWorld := "Hello World"
	if helloWorld != "Hello World" {
		t.Errorf("Uh oh!")
	}
}
