package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)

// ReadInput reads input from the CLI and tries to parse it into the type of the provided variable
func ReadInput(prompt string, target interface{}) error {
    fmt.Print(prompt)
    reader := bufio.NewReader(os.Stdin)
    input, err := reader.ReadString('\n')
    if err != nil {
        return fmt.Errorf("failed to read input: %w", err)
    }

    // Trim whitespace and newlines
    input = strings.TrimSpace(input)

    // Type assertion to handle different target types
    switch v := target.(type) {
    case *int:
        // Convert to int
        num, err := strconv.Atoi(input)
        if err != nil {
            return fmt.Errorf("invalid integer input: %w", err)
        }
        *v = num
    case *float64:
        // Convert to float64
        num, err := strconv.ParseFloat(input, 64)
        if err != nil {
            return fmt.Errorf("invalid float input: %w", err)
        }
        *v = num
    case *string:
        // No conversion needed for strings
        *v = input
    default:
        return fmt.Errorf("unsupported type")
    }

    return nil
}

func main() {
    var intValue int
    var floatValue float64
    var stringValue string

    // Get an integer input
    if err := ReadInput("Enter an integer: ", &intValue); err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("You entered integer:", intValue)
    }

    // Get a float input
    if err := ReadInput("Enter a float: ", &floatValue); err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("You entered float:", floatValue)
    }

    // Get a string input
    if err := ReadInput("Enter a string: ", &stringValue); err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("You entered string:", stringValue)
    }
}
