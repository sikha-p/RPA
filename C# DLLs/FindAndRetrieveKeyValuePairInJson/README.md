# Searching for a Key-Value Pair Within a JSON Object Subtree Based on a Parent Key


**Scenario**: 
- Let's assume that you are working with complex JSON data structures representing hierarchical information such as transactions with nested documents, fields, and annotations. For example, a JSON object may contain a "Transaction" element, which further nests arrays and objects like "Documents", "ExtractedData" and "RootObject".

**Solution**:
- This is a DLL solution which can be used inside A360 Bot.  The A360 bot has 2 dependencies as shown in the image below. SearchAndGetKeyValueFromJson.dll is the main DLL & the Newtonsoft.Json.dll  is the dependent one. 


This DLL solution provides a way to search and retrieve the value of a target key by:

Locating the parent JSON object by its key anywhere in the JSON hierarchy.
Recursively searching within this parent object for a nested object that contains the specified key-value pair.
Extracting the value of the target key from the matched nested object.

This approach abstracts away the complexity of the JSON structure, such as unknown nesting levels or array indices, enabling flexible and dynamic querying of deeply nested JSON data.





**How the Solution Works**

- The solution consists of several key steps implemented as recursive searches:

- #### Finding the Parent Object:
  -  A recursive search traverses the JSON tree to find the first JSON object with the specified parent key. This ensures the search is scoped to the relevant subtree.

- #### Finding the Object with the Matching Key-Value Pair:
  -  Within the parent object, another recursive search looks for any nested object that contains the searchKey with the exact searchValue . This allows pinpointing the precise object of interest regardless of its depth or position.
- ##### Retrieving the Target Value:
  -  After locating the matched object, a final recursive search extracts the value associated with the targetKey within that object.

**Example Use Case**

Consider the JSON structure representing a transaction with nested documents and extracted data fields. Using this solution, you can:

- ##### Search under the "RootObject" key. 
- ##### Find the object where  "Name" equals "DummyName4" .
- ##### Retrieve the corresponding "Value" key's value from that object. eg: "DummyValue4".



**Note:**

If you need, this solution can be adapted or extended for additional querying needs or integrated into broader data processing workflows.

Sample JSON 
```
{
  "Version": "1.1",
  "Transaction": {
    "Id": "***********************",
    "SkillId": "***********************",
    "SkillName": "DummySkillName-1",
    "Documents": [
      {
        "Id": "***********************",
        "ExtractedData": {
          "DocumentDefinition": {
            "RootConcept": {
              "Id": "root",
              "Name": "DummyName1",
              "Fields": [
                {
                  "Id": "***********************",
                  "Name": "DummyName2",
                  "Type": "String",
                  "Cardinality": {
                    "Min": 0,
                    "Max": 1
                  }
                },
                {
                  "Id": "***********************",
                  "Name": "DummyName3",
                  "Type": "String",
                  "Cardinality": {
                    "Min": 0,
                    "Max": 1
                  }
                }
              ]
            }
          },
          "RootObject": {
            "Id": "root",
            "Concept": "DUMMY-Concept",
            "Fields": [
              {
                "Name": "DummyName4",
                "List": [
                  {
                    "Id": "***********************",
                    "Annotations": [
                      {
                        "Source": "Image",
                        "ImageRegions": [
                          {
                            "Page": "***********************",
                            "Rects": [
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]
                            ]
                          }
                        ],
                        "RawValue": "DUMMY-Raw value6",
                        "SuspiciousSymbols": []
                      }
                    ],
                    "Value": "DummyValue4"
                  }
                ]
              },
              {
                "Name": "DummyName7",
                "List": [
                  {
                    "Id": "***********************",
                    "Annotations": [
                      {
                        "Source": "Image",
                        "ImageRegions": [
                          {
                            "Page": "***********************",
                            "Rects": [
                              [0, 0, 0, 0]
                            ]
                          }
                        ],
                        "RawValue": "DUMMY-Raw value5",
                        "SuspiciousSymbols": []
                      }
                    ],
                    "Value": "DummyValue7"
                  }
                ]
              },
              {
                "Name": "DummyName8",
                "List": [
                  {
                    "Id": "***********************",
                    "Annotations": [
                      {
                        "Source": "Image",
                        "ImageRegions": [
                          {
                            "Page": "***********************",
                            "Rects": [
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]
                            ]
                          }
                        ],
                        "RawValue": "DUMMY-Raw value4",
                        "SuspiciousSymbols": []
                      }
                    ],
                    "Value": "DummyValue8"
                  }
                ]
              },
              {
                "Name": "DummyName9",
                "List": [
                  {
                    "Id": "***********************",
                    "Annotations": [
                      {
                        "Source": "Image",
                        "ImageRegions": [
                          {
                            "Page": "***********************",
                            "Rects": [
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]
                            ]
                          }
                        ],
                        "RawValue": "DUMMY-Raw value3",
                        "SuspiciousSymbols": []
                      }
                    ],
                    "Value": "DummyValue9"
                  }
                ]
              },
              {
                "Name": "DummyName10",
                "List": [
                  {
                    "Id": "***********************",
                    "Annotations": [
                      {
                        "Source": "None",
                        "RawValue": "DUMMY-Raw value2"
                      }
                    ],
                    "Value": "DummyValue10"
                  }
                ]
              },
              {
                "Name": "DummyName11",
                "List": [
                  {
                    "Id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "Annotations": [
                      {
                        "Source": "None",
                        "RawValue": "DUMMY-Raw value1"
                      }
                    ],
                    "Value": "DummyValue11"
                  }
                ]
              }
            ]
          }
        },
        "Pages": [
          {
            "Id": ".***********************",
            "SourceFile": "DUMMYPDF.pdf",
            "SourceImagePageIndex": 1
          }
        ],
        "CreationTime": "xxxx-xx-xxTxx:xx:xx.xxxxxx+xx:xx",
        "SourceFiles": [
          {
            "Id": ".***********************",
            "Name": "dummypdf2pdf"
          }
        ]
      }
    ]
  }
}
```
