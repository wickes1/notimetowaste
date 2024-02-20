# Python Data Format

## Comparison of Serialization and Schema Formats

| Trait            | Avro                                   | Protobuf                                | JSON Schema                                  | Thrift                                  | Apache Arrow                                             | Apache Parquet                    | Apache ORC                        |
| ---------------- | -------------------------------------- | --------------------------------------- | -------------------------------------------- | --------------------------------------- | -------------------------------------------------------- | --------------------------------- | --------------------------------- |
| Serialization    | Binary, compact, schema-aware          | Binary, efficient, schema-aware         | N/A                                          | Binary, efficient, schema-aware         | Columnar, in-memory data representation                  | Columnar, on-disk storage         | Columnar, on-disk storage         |
| Language         | Language-independent                   | Language-independent                    | Language-independent                         | Cross-language (but tied to Thrift)     | Cross-language (but primarily used in Python, C++, Java) | Language-independent              | Language-independent              |
| Schema Evolution | Supports schema evolution              | Supports backward/forward compatibility | N/A                                          | Supports backward/forward compatibility | N/A                                                      | Supports schema evolution         | Supports schema evolution         |
| Code Generation  | Code generation for specific languages | Code generation for multiple languages  | N/A                                          | Code generation for specific languages  | N/A                                                      | N/A                               | N/A                               |
| Data Validation  | Schema validation                      | N/A                                     | Schema validation                            | N/A                                     | N/A                                                      | N/A                               | N/A                               |
| Usage            | Commonly used in big data processing   | Commonly used in distributed systems    | Commonly used in API design, data validation | Commonly used in distributed systems    | Commonly used for in-memory data processing              | Commonly used for on-disk storage | Commonly used for on-disk storage |

## [Avro](https://avro.apache.org/)

```json
{
    "name": "ReaderWriterSchema",
    "type": "record",
    "namespace": "com",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "value", "type": "string"},
    ],
}
```

```json
 {
    "name": "ReaderWriterSchema",
    "type": "record",
    "namespace": "com",
    "fields": [
        {"name": "eid", "aliases": ["id"], "type": "int"},
        {"name": "reader_new_name", "aliases": ["name"], "type": "string"},
    ],
}
```

## [Protobuf](https://protobuf.dev/)

```protobuf
syntax = "proto3";

message Data {
    int32 id = 1;
    string name = 2;
    string value = 3;
}
```

```bash
# Generate Python code
protoc --python_out=. data.proto
```

## [Thrift](https://thrift.apache.org/)

```thrift
namespace py example

struct Person {
  1: string name,
  2: i32 age,
  3: string email
}

service PersonService {
  void addPerson(1: Person person),
  Person getPerson(1: string name)
}
```

```bash
# Generate python code
thrift --gen py example.thrift
```

## [JSON Schema](https://json-schema.org/)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    },
    "name": {
      "type": "string"
    },
    "value": {
      "type": "string"
    }
  },
  "required": ["id", "name", "value"]
}
```

## FAQ

### How to do error handling?

Data format with schema validation can be used to ensure data quality. For example, Avro, Protobuf, and JSON Schema support schema validation. We may use the methods below to handle errors:

1. Try-Except Blocks: Use try-except blocks to catch validation errors and handle them gracefully.
2. Error Messages: schema library error messages include detailed information about why validation failed. Use this information to generate clear, actionable feedback.
3. Logging: In a development or debugging context, logging the details of validation errors can be incredibly helpful for diagnosing issues.

### Where to integrate the schema?

1. API Request Validation: Use schema to validate incoming requests in web APIs. This ensures that the data conforms to the expected format before processing.
2. Configuration Files: Validate configuration files against a schema to catch errors early and avoid runtime issues.
3. Data Processing: In applications that process large volumes of data, use schema to validate data before processing to ensure it meets the necessary criteria. Also use schema to serialize and deserialize data to shrink the data size on the wire.

## References

Kleppmann, Martin. *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*.O'Reilly Media, 2017.
