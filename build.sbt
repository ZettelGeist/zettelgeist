// name := "simplemap-spark-scala"

version := "1.0"

scalaVersion := "2.11.11"

scalacOptions ++= Seq("-deprecation", "-feature", "-unchecked")

// mainClass in assembly := Some("dataflows.spark.SparkBenchmarkHPC")

resolvers ++= Seq(
  "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
)

val circeVersion = "0.8.0"
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core",
  "io.circe" %% "circe-generic",
  "io.circe" %% "circe-parser"
).map(_ % circeVersion)

libraryDependencies ++= Seq(
  "com.github.scopt" %% "scopt" % "3.4.0",
  "org.json4s" %% "json4s-native" % "3.3.0",
  "org.json4s" %% "json4s-jackson" % "3.3.0",
  "io.circe" %% "circe-yaml" % "0.6.1",
  "com.novocode" % "junit-interface" % "latest.release" % Test,
  "org.scalatest" %% "scalatest" % "latest.release" % Test
)

