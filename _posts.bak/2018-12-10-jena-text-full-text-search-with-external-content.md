---
title: Example of apache jena-text full text search with external content using Apache Lucene
date: 2018-12-14
writing-time: 2018-12-10--2018-12-14
categories: rdf
tags: rdf sparql jena-text lucene
---

# Introduction

According to document [Jena Full Text Search](https://jena.apache.org/documentation/query/text-query.html#external-content), it is possible that the indexed text is content external to the RDF store with only additional triples in the RDF store. The subject URI returned as a search result may then be considered to refer via the indexed property to the external content.

To work with external content, the maintenance of the index is external to the RDF data store too. The key of the index is: building an `URI` field from indexed document's path.

When the text search is performed, the `URIs` returned as the search result will be used for matching the subject URI in the SPARQL query.

In this tutorial, we create lucene index for external text documents, perform a full text search in SPARQL using jena-text, then return the highlighting results.

The example code is available on [github](https://github.com/haiiiiiyun/jena-text-full-text-search-with-external-content).

# Create Maven project

The example project uses `jena-text` 3.9.0 and `lucene` 6.4.2(the lucene dependencey is already specified in the jena-text library).

Add the following depedecies to you pom.xml:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.atjiang.jena</groupId>
  <artifactId>jena-text-full-text-search-with-external-content</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>jena-text-full-text-search-with-external-content</name>
  <url>http://maven.apache.org</url>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-antrun-plugin</artifactId>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.0</version>
        <configuration>
          <source>1.7</source>
          <target>1.7</target>
        </configuration>
      </plugin>
      <plugin>
        <artifactId>maven-dependency-plugin</artifactId>
        <executions>
          <execution>
            <phase>install</phase>
            <goals>
              <goal>copy-dependencies</goal>
            </goals>
            <configuration>
              <outputDirectory>${project.build.directory}/lib</outputDirectory>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.apache.jena</groupId>
      <artifactId>apache-jena-libs</artifactId>
      <type>pom</type>
      <version>3.9.0</version>
    </dependency>

    <dependency>
      <groupId>org.apache.jena</groupId>
      <artifactId>jena-cmds</artifactId>
      <version>3.9.0</version>
    </dependency>

    <!-- https://mvnrepository.com/artifact/org.apache.jena/jena-text -->
    <dependency>
      <groupId>org.apache.jena</groupId>
      <artifactId>jena-text</artifactId>
      <version>3.9.0</version>
    </dependency>


    <!-- Testing support -->
    <dependency>
      <groupId>org.apache.jena</groupId>
      <artifactId>jena-base</artifactId>
      <version>3.9.0</version>
      <classifier>tests</classifier>
      <scope>test</scope>
    </dependency>

    <!-- https://mvnrepository.com/artifact/org.apache.maven.plugins/maven-compiler-plugin -->
    <dependency>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.8.0</version>
    </dependency>
  </dependencies>
</project>
```

# Example data

The turtle file called `data.ttl` is stored in the root directory of the project, which is searched in SPARQL.

```turtle
@prefix email: <http://atjiang.com/data/email/> .

<http://atjiang.com/data/email/id/id1> email:content "no_matter_what.txt" .
<http://atjiang.com/data/email/id/id2> email:content "no_matter_what.txt" .
```

The text files under directory `to_index` are the external files which will be used to create a Lucene index. File name of each text file is the email id, corresponding to the email id in the turtle file. 

```bash
$ ls -la to_index/
total 16
drwxrwxr-x 2 hy hy 4096 12月  6 08:44 .
drwxrwxr-x 7 hy hy 4096 12月 13 15:06 ..
-rw-rw-r-- 1 hy hy   30 12月  6 08:44 id1
-rw-rw-r-- 1 hy hy   28 12月  6 08:44 id2

$ cat to_index/id1
context 
good luck
background

$ cat to_index/id2
context
bad luck
background
```

# Code example explained

The lucene index and search code are based on Lucene's demo code [IndexFiles.java](http://lucene.apache.org/core/7_5_0/demo/src-html/org/apache/lucene/demo/IndexFiles.html) and [SearchFiles.java](http://lucene.apache.org/core/7_5_0/demo/src-html/org/apache/lucene/demo/SearchFiles.html).


## Create lucene index

```java
// in file IndexFiles.java
  /** Indexes a single document */
  static void indexDoc(IndexWriter writer, Path file, long lastModified) throws IOException {
    try (InputStream stream = Files.newInputStream(file)) {
      // make a new, empty document
      Document doc = new Document();
      
      // Add the path of the file as a field named "path".  Use a
      // field that is indexed (i.e. searchable), but don't tokenize 
      // the field into separate words and don't index term frequency
      // or positional information:
      Field pathField = new StringField("uri", App.EMAIL_URI_PREFIX + "id/" + file.getFileName().toString(), Field.Store.YES);
      doc.add(pathField);
      
      // Add the last modified date of the file a field named "modified".
      // Use a LongPoint that is indexed (i.e. efficiently filterable with
      // PointRangeQuery).  This indexes to milli-second resolution, which
      // is often too fine.  You could instead create a number based on
      // year/month/day/hour/minutes/seconds, down the resolution you require.
      // For example the long value 2011021714 would mean
      // February 17, 2011, 2-3 PM.
      doc.add(new LongPoint("modified", lastModified));
      
      // Add the contents of the file to a field named "contents".  Specify a Reader,
      // so that the text of the file is tokenized and indexed, but not stored.
      // Note that FileReader expects the file to be in UTF-8 encoding.
      // If that's not the case searching for special characters will fail.
      //doc.add(new TextField("text", new BufferedReader(new InputStreamReader(stream, StandardCharsets.UTF_8))));
      doc.add(new TextField("text", new String(Files.readAllBytes(file)), Field.Store.YES));


      if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
        // New index, so we just add the document (no old document can be there):
        System.out.println("adding " + file);
        writer.addDocument(doc);
      } else {
        // Existing index (an old copy of this document may have been indexed) so 
        // we use updateDocument instead to replace the old one matching the exact 
        // path, if present:
        System.out.println("updating " + file);
        writer.updateDocument(new Term("path", file.toString()), doc);
      }
    }
  }
}
```

With in line `Field pathField = new StringField("uri", App.EMAIL_URI_PREFIX + "id/" + file.getFileName().toString(), Field.Store.YES);`, we create a StringField `uri` from the external text file's name. And `Field.Store.YES` indicates the text file's content will be stored in the index, which is used for working with jena-text's  full text search highlighting feature.


## Load dataset and define the index mapping

```java
// in file JenaTextSearch.java

public static Dataset createCode() 
{
    // Base data
    Dataset ds1 = DatasetFactory.create() ;
    Model defaultModel = ModelFactory.createDefaultModel();
    defaultModel.read("data.ttl", "N-TRIPLES");
    ds1.setDefaultModel(defaultModel);

    // Define the index mapping
    EntityDefinition entDef = new EntityDefinition( "uri", "text", ResourceFactory.createProperty( App.EMAIL_URI_PREFIX, "content" ) );

    Directory dir = null;
    try {
        dir = new SimpleFSDirectory(Paths.get("index")); // lucene index directory
    }
    catch( IOException e){
        e.printStackTrace();
    }

    // Join together into a dataset
    Dataset ds = TextDatasetFactory.createLucene( ds1, dir, new TextIndexConfig(entDef) ) ;
    
    return ds ;
}
```

We define the index mapping according to the index we built. The index itself is maintained by the main app, see code in below.


## jena-text query

```java
public static void queryData(Dataset dataset)
{
    String prefix = "PREFIX email: <" + App.EMAIL_URI_PREFIX + "> " +
            "PREFIX text: <http://jena.apache.org/text#> ";

    long startTime = System.nanoTime() ;
    System.out.println("Email's content contains 'good'");
    String query = "SELECT * WHERE " +
            "{ ?s text:query (email:content 'good') ." +
            "  ?s email:content ?text . " +
            " }";

    dataset.begin(ReadWrite.READ) ;
    try {
        Query q = QueryFactory.create(prefix+"\n"+query) ;
        QueryExecution qexec = QueryExecutionFactory.create(q , dataset) ;
        QueryExecUtils.executeQuery(q, qexec) ;
    } finally { dataset.end() ; }
    long finishTime = System.nanoTime() ;
    double time = (finishTime-startTime)/1.0e6 ;
    System.out.println("Query " + String.format("FINISH - %.2fms", time)) ;

    startTime = System.nanoTime() ;
    System.out.println("Email's content contains 'bad'");
    query = "SELECT * WHERE " +
            "{ (?s ?score ?lit) text:query (email:content 'bad' \"highlight:s:<em class='hiLite'> | e:</em>\") ." +
            "  ?s email:content ?text . " +
            " }";

    dataset.begin(ReadWrite.READ) ;
    try {
        Query q = QueryFactory.create(prefix+"\n"+query) ;
        QueryExecution qexec = QueryExecutionFactory.create(q , dataset) ;
        QueryExecUtils.executeQuery(q, qexec) ;
    } finally { dataset.end() ; }
    finishTime = System.nanoTime() ;
    time = (finishTime-startTime)/1.0e6 ;
    System.out.println("Query " + String.format("FINISH - %.2fms", time)) ;
}
```


## The main entry

```java
// in file App.java
public class App
{
    static String EMAIL_URI_PREFIX = "http://atjiang.com/data/email/";
    public static void main( String[] args ) {

        testJenaText();
    }

    public static void testJenaText() {
        IndexFiles.testIndex();
        try {
            SearchFiles.testSearch();
        } catch (Exception e){

            System.out.println(e.toString());
        }

        JenaTextSearch.main();
    }
}
```

# Compile and run

```bash
$ mvn install
$ mvn compile
$ java -cp target/jena-text-full-text-search-with-external-content-1.0-SNAPSHOT.jar:target/lib/* com.atjiang.jena.App


Indexing to directory 'index'...
adding to_index/id1
adding to_index/id2
357 total milliseconds
Searching for: luck
2 total matching documents
1. http://atjiang.com/data/email/id/id1
2. http://atjiang.com/data/email/id/id2
log4j:WARN No appenders could be found for logger (org.apache.jena.util.FileManager).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.
Email's content contains 'good'
-----------------------------------------------------------------
| s                                      | text                 |
=================================================================
| <http://atjiang.com/data/email/id/id1> | "no_matter_what.txt" |
-----------------------------------------------------------------
Query FINISH - 159.10ms
Email's content contains 'bad'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| s                                      | score                                                 | lit                                                       | text                 |
=====================================================================================================================================================================================
| <http://atjiang.com/data/email/id/id2> | "0.6931472"^^<http://www.w3.org/2001/XMLSchema#float> | "context\n<em class='hiLite'>bad</em> luck\nbackground\n" | "no_matter_what.txt" |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Query FINISH - 17.91ms

```


# Lucene index tools

You can analyze the Lucene index using the [Luke](https://github.com/DmitryKey/luke) toolbox. With this toolbox, you can see how many terms are indexed, with what frequency they occur.


# Resources

+ [Jena Full Text Search](https://jena.apache.org/documentation/query/text-query.html#external-content)
+ [Apache Lucene - Building and Installing the Basic Demo](http://lucene.apache.org/core/7_5_0/demo/overview-summary.html#overview.description)
+ [Full text search in SPARQL using Apache Lucene](https://tutorial-academy.com/full-text-search-sparql-lucene/)
+ https://github.com/DmitryKey/luke
