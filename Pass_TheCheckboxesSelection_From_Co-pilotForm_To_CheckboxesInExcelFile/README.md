# How to pass the checkboxes selection from Co-pilot form to a checkboxes in excel file

Assume you have a Co-pilot process and the FORM inside the process has a checkbox group in it. You need to transfer the checkbox group selection to your local Excel file. This solution will guide you on how to accomplish that. 

### Pre requisites

* We need to use a macro function to make this work. So your Excel file should be a Macro-enabled spreadsheet (.xlsm) file with a macro function encapsulated in it .


### This solution passes the checkbox group selection details from the co-pilot FORM to an A360 Bot inside the process. The A360 Bot will run a Macro function to set the checkboxes values in a local Excel file as per the input from the co-pilot FORM.


```
Sub SelectCheckboxesByLabels(sParam1 As String, sParam2 As String, sParam3 As String, sParam4 As String)
    Dim chk As Object
    Dim ws As Worksheet
    Dim i As Integer
    Dim params As Variant
    Dim label As String
    Dim state As Boolean

    Set ws = ThisWorkbook.Sheets("Sheet1") ' Change "Sheet1" to your sheet's name

    ' Combine parameters into an array
    params = Array(sParam1, sParam2, sParam3, sParam4)

    ' Iterate through each parameter
    For i = LBound(params) To UBound(params)
        label = Split(params(i), "=")(0)
        state = CBool(Split(params(i), "=")(1))

        ' Iterate through all checkboxes in the sheet
        For Each chk In ws.CheckBoxes
            If chk.Text = label Then
                If state Then
                    chk.Value = xlOn
                Else
                    chk.Value = xlOff
                End If
            End If
        Next chk
    Next i
End Sub

```

## Authors

Contributors names and contact info

1. Sikha Poyyil

