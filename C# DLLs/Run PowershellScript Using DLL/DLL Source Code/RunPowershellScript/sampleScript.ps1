try{
    $allargs = $args[0].Split(";")
    $input1 = $allargs[0]
    $input2 = $allargs[1]
     # Concatenate input1 and input2
    $result = "$input1 $input2"

    # Output the concatenated result
    Write-Output $result
}
catch{
    #Handle error
    Write-Output "Error Details: $($_.Exception.Message)"
}