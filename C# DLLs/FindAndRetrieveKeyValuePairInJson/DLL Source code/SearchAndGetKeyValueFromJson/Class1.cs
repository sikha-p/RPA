using System;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace SearchAndGetKeyValueFromJson
{
    public class Class1
    {
        /// <summary>
        /// Recursively searches for a JObject with the specified key anywhere in the JSON token.
        /// Returns the JObject corresponding to the key if found; otherwise, null.
        /// </summary>
        public static JObject FindJObjectByKey(JToken token, string key)
        {
            if (token == null) return null;

            if (token is JObject obj)
            {
                foreach (var property in obj.Properties())
                {
                    if (property.Name == key && property.Value is JObject foundObj)
                        return foundObj;

                    var result = FindJObjectByKey(property.Value, key);
                    if (result != null)
                        return result;
                }
            }
            else if (token is JArray arr)
            {
                foreach (var item in arr)
                {
                    var result = FindJObjectByKey(item, key);
                    if (result != null)
                        return result;
                }
            }

            return null;
        }

        /// <summary>
        /// Recursively searches for a JObject that contains a key-value pair (searchKey=searchValue).
        /// Returns the JObject if found; otherwise, null.
        /// </summary>
        private static JObject FindObjectWithKeyValue(JToken token, string searchKey, string searchValue)
        {
            if (token == null) return null;

            if (token is JObject obj)
            {
                if (obj.TryGetValue(searchKey, out JToken val) && string.Equals(val?.ToString(), searchValue, StringComparison.Ordinal))
                    return obj;

                foreach (var property in obj.Properties())
                {
                    var found = FindObjectWithKeyValue(property.Value, searchKey, searchValue);
                    if (found != null)
                        return found;
                }
            }
            else if (token is JArray arr)
            {
                foreach (var item in arr)
                {
                    var found = FindObjectWithKeyValue(item, searchKey, searchValue);
                    if (found != null)
                        return found;
                }
            }

            return null;
        }

        /// <summary>
        /// Recursively searches the JSON token for a key and returns its value if found.
        /// Returns null if the key is not found.
        /// </summary>
        private static JToken FindKey(JToken token, string key)
        {
            if (token == null) return null;

            if (token is JObject obj)
            {
                foreach (var property in obj.Properties())
                {
                    if (property.Name == key)
                        return property.Value;

                    var found = FindKey(property.Value, key);
                    if (found != null)
                        return found;
                }
            }
            else if (token is JArray arr)
            {
                foreach (var item in arr)
                {
                    var found = FindKey(item, key);
                    if (found != null)
                        return found;
                }
            }

            return null;
        }

        /// <summary>
        /// Parses the JSON string and searches within the subtree under a parent key,
        /// for an object containing a key-value pair, and returns the value of a target key in that object.
        /// This method does not require a listKey and searches recursively inside the parent.
        /// </summary>
        public static string FindandRetriveKeyValuePairInJson(
            string json, string parentKey,
            string searchKey, string searchValue, string targetKey)
        {
            if (string.IsNullOrWhiteSpace(json))
                throw new ArgumentException("JSON input cannot be null or empty.", nameof(json));

            try
            {
                var root = JObject.Parse(json);
                JObject parent = FindJObjectByKey(root, parentKey);
                if (parent == null)
                    return null;

                var matchedObject = FindObjectWithKeyValue(parent, searchKey, searchValue);
                if (matchedObject == null)
                    return null;

                var targetValueToken = FindKey(matchedObject, targetKey);
                return targetValueToken?.ToString();
            }
            catch (JsonReaderException jex)
            {
                Console.Error.WriteLine($"JSON parsing error: {jex.Message}");
                return $"JSON parsing error: {jex.Message}";
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Unexpected error: {ex.Message}");
                return $"Unexpected error: {ex.Message}";
            }
        }
    }
}