function step201 {
    # Hardcoded input
    $number = -5
    Write-Output "Checking if $number is negative"
    return ($number -lt 0)
}

function step202 {
    # Hardcoded inputs
    $a = 10
    $b = 20
    $sum = $a + $b
    Write-Output "step202: $a + $b = $sum"
    return $sum
}

function step203 {
    # Hardcoded inputs
    $a = 30
    $b = 12
    $difference = $a - $b
    Write-Output "step203: $a - $b = $difference"
    return $difference
}

function run {
    $step201_result = step201
    Write-Output "step201 $step201_result"
    if ($step201_result) {
        $step202_result = step202
        Write-Output "step202 $step202_result"
    } else {
        $step203_result = step203
        Write-Output "step203 $step201_result"
    }
    $step202_result = step202
    $step203_result = step203
}

run