// name := "simplemap-spark-scala"

version := "1.0"

scalaVersion := "2.11.11"

scalacOptions ++= Seq("-deprecation", "-feature", "-unchecked")

// mainClass in assembly := Some("dataflows.spark.SparkBenchmarkHPC")

resolvers ++= Seq(
  "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
)

libraryDependencies ++= Seq(
  "com.github.scopt" %% "scopt" % "3.4.0",
  "org.json4s" %% "json4s-native" % "3.3.0",
  "org.json4s" %% "json4s-jackson" % "3.3.0",
  "com.novocode" % "junit-interface" % "latest.release" % Test,
  "org.scalatest" %% "scalatest" % "latest.release" % Test
)
