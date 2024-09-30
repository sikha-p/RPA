using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Xceed.Document.NET;
using Xceed.Words.NET;
using Excel = Microsoft.Office.Interop.Excel;


namespace TablesInWordDocToExcel
{
    public class Class1
    {
        public static string ReadDocxTable(string docxFilePath, string excelFilePath)
        {
            try
            {
                List<Dictionary<string, object>> finalJsonArray = new List<Dictionary<string, object>>();

                var excelApp = new Excel.Application();
                var workbook = excelApp.Workbooks.Add();

                using (DocX document = DocX.Load(docxFilePath))
                {
                    for (int tableIndex = 0; tableIndex < document.Tables.Count; tableIndex++)
                    {
                        DataTable dataTable = new DataTable();
                        Table table = document.Tables[tableIndex];

                        if (table != null)
                        {
                            List<string> orderedColumnNames = new List<string>();

                            Row headerRow = table.Rows.FirstOrDefault();
                            if (headerRow != null)
                            {
                                Dictionary<string, int> columnNameCount = new Dictionary<string, int>();

                                foreach (Cell cell in headerRow.Cells)
                                {
                                    string columnName = string.Join(" ", cell.Paragraphs.Select(p => p.Text.Trim()));

                                    if (string.IsNullOrWhiteSpace(columnName))
                                    {
                                        columnName = "Column";
                                    }

                                    if (columnNameCount.ContainsKey(columnName))
                                    {
                                        columnNameCount[columnName]++;
                                        columnName = $"{columnName}_{columnNameCount[columnName]}";
                                    }
                                    else
                                    {
                                        columnNameCount[columnName] = 1;
                                    }

                                    orderedColumnNames.Add(columnName);
                                    dataTable.Columns.Add(columnName);
                                }

                                foreach (Row row in table.Rows.Skip(1))
                                {
                                    DataRow dataRow = dataTable.NewRow();
                                    for (int i = 0; i < orderedColumnNames.Count; i++)
                                    {
                                        if (i < row.Cells.Count)
                                        {
                                            dataRow[orderedColumnNames[i]] = string.Join(" ", row.Cells[i].Paragraphs.Select(p => p.Text.Trim()));
                                        }
                                        else
                                        {
                                            dataRow[orderedColumnNames[i]] = "";
                                        }
                                    }
                                    dataTable.Rows.Add(dataRow);
                                }
                            }

                            string sts = RemoveColumnsWithAllNulls(dataTable);
                            if (sts.Contains("ERROR"))
                            {
                                return sts;

                            }
                            var newObject = new Dictionary<string, object>
                           {
                              { "table_" + tableIndex.ToString(),  JsonConvert.SerializeObject(dataTable) }
                            };
                            finalJsonArray.Add(newObject);

                            // Add the DataTable to the Excel workbook
                            var worksheet = (Excel.Worksheet)workbook.Worksheets.Add();
                            worksheet.Name = $"Table_{tableIndex + 1}";

                            // Add column headers
                            for (int col = 0; col < dataTable.Columns.Count; col++)
                            {
                                worksheet.Cells[1, col + 1] = dataTable.Columns[col].ColumnName;
                            }

                            // Add rows
                            for (int row = 0; row < dataTable.Rows.Count; row++)
                            {
                                for (int col = 0; col < dataTable.Columns.Count; col++)
                                {
                                    worksheet.Cells[row + 2, col + 1] = dataTable.Rows[row][col].ToString();
                                }
                            }
                        }
                    }
                }

                // Save the Excel file
                workbook.SaveAs(excelFilePath);
                workbook.Close();
                excelApp.Quit();

                string finalJsonString = JsonConvert.SerializeObject(finalJsonArray, Newtonsoft.Json.Formatting.Indented);
                string json = "{ \"list\" : " + finalJsonString + "}";
                return json;
            }
            catch(Exception ex)
            {
                return "ERROR: " + ex.Message;
            }
           
        }

        static string RemoveColumnsWithAllNulls(DataTable dataTable)
        {
            try
            {
                var columnsToRemove = new List<DataColumn>();

                foreach (DataColumn column in dataTable.Columns)
                {
                    bool allNulls = true;

                    foreach (DataRow row in dataTable.Rows)
                    {
                        if (row[column] != DBNull.Value && !string.IsNullOrWhiteSpace(row[column].ToString()))
                        {
                            allNulls = false;
                            break;
                        }
                    }

                    if (allNulls)
                    {
                        columnsToRemove.Add(column);
                    }
                }

                foreach (var column in columnsToRemove)
                {
                    dataTable.Columns.Remove(column);
                }
                return "success";
            }
            catch(Exception ex)
            {
                return "ERROR: "+ ex.Message;
            }
            
        }
    }
}
