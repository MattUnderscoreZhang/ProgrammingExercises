package main

import (
    "fmt"
    "errors"
)

func add(a float64, b float64) float64 {
    return a + b
}

func subtract(a float64, b float64) float64 {
    return a - b
}

func multiply(a float64, b float64) float64 {
    return a * b
}

func divide(a float64, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("Cannot divide by zero")
    }
    return a / b, nil
}

func main() {
    var a, b float64

    err := errors.New("An error")
    for err != nil {
        fmt.Print("Enter a: ")
        _, err = fmt.Scan(&a)
        if err != nil {
            fmt.Println(err)
            var discard string
            fmt.Scanln(&discard)
        }
    }

    err = errors.New("An error")
    for err != nil {
        fmt.Print("Enter b: ")
        _, err = fmt.Scan(&b)
        if err != nil {
            fmt.Println(err)
            var discard string
            fmt.Scanln(&discard)
        }
    }

    fmt.Println("a + b =", add(a, b))
    fmt.Println("a - b =", subtract(a, b))
    fmt.Println("a * b =", multiply(a, b))

    result, err := divide(a, b)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("a / b =", result)
    }
}
