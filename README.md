### coblr
cobble together a database from a set of spreadsheets. simply specify a schema using your filesystem and copy your spreadsheets to where they fit in your schema. colbr assumes that you are running a local postgres server.

Usage:

```
  coblr cobble new_database_name schema/
```


```
schema
├── ns1
│   └── transactions
│       ├── txns1.csv
│       └── txns2.csv
└── ns2
    └── transactions
        ├── txns1.csv
        └── txns2.csv
```

Given this directory structure and set of files, ```coblr cobble``` will create a database with namespaces ns1 and ns2, each with a table called transactions.  The tables' columns are derived from the column headers in the spreadsheets.  The records from the spreadsheets are then loaded into the database.


### todo
- infer field types rather than unicodifying blindly
- detect relationships and construct foreign keys
- add framework for massaging spreadsheets prior to ingestion
