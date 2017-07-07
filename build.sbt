name := "zettelgeist"

version := "1.0"

scalaVersion := "2.12.2"

scalacOptions ++= Seq("-deprecation", "-feature", "-unchecked")

mainClass in assembly := Some("zettelgeist.Import")

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
  "io.circe" %% "circe-yaml" % "0.6.1",
  "org.json4s" %% "json4s-native" % "3.5.2",
  "org.json4s" %% "json4s-jackson" % "3.5.2",
  "com.github.scopt" %% "scopt" % "3.6.0",
  "com.novocode" % "junit-interface" % "latest.release" % Test,
  "org.scalatest" %% "scalatest" % "latest.release" % Test,
  "com.github.tototoshi" %% "scala-csv" % "1.3.4",
  "com.lihaoyi" %% "ammonite-ops" % "1.0.0"
)

