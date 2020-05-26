struct Card
    front::String
    back::String

    function Card(front::String, back::String)
        new(front, back)
    end
end


cards = []
filename = "001.dat"
open(filename, "r") do file
    linetype = 0
    local question, answer
    for line in eachline(file)
        if (linetype == 0)
            question = line
        elseif (linetype == 1)
            answer = line
            card = Card(question, answer)
            push!(cards, card)
        end
        linetype = (linetype+1)%3
    end
end


for card in cards
    println("$(card.front)")
    print("Answer: ")
    readline()
    println("$(card.back)")
    println()
end
