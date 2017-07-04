package zettelgeist

import ammonite.ops._
import org.scalatest._
import io.circe.Error
import org.json4s.jackson.JsonMethods._
import cats.syntax.either._
import io.circe.generic.auto._
import io.circe.yaml
import java.io._

class ZettelParsingTests extends FlatSpec with Matchers {

  "Circe YAML Experiments" should "run this slightly-modified example from their own docs" in {

    case class Nested(one: String, two: BigDecimal)
    case class Foo(foo: String, bar: Nested, baz: List[String], extra1: Option[String], extra2: Option[String])

    val json = yaml.parser.parse(
      """
       |foo: Hello, World
       |bar:
       |  one: One Third
       |  two: 33.333333
       |baz:
       |- Hello
       |- World
       |extra2: extra2""".
      stripMargin
    )

    val foo = json
      .leftMap(err => err: Error)
      .flatMap(_.as[Foo])
      .valueOr(throw _)

    foo.foo should be("Hello, World")
    foo.bar should be(Nested("One Third", BigDecimal("33.333333")))
    foo.baz should be(List("Hello", "World"))
    foo.extra1 should be(None)
    foo.extra2 should be(Some("extra2"))
  }

  it should "be able to bind to case class Zettel (domain object)" in {
    val json = yaml.parser.parse(
      """
       |title: My First Zettel
       |mentions:
       |- dbdennis
       |- gkt
       |tags:
       |- Charles Babbage
       |- Ada Lovelace
       |cite:
       |  bibkey: Ifrah
       |  page: 22
       |  last_page: 36
       |dates:
       |  year: 1841
       |  era: CE
       |summary: An amazing Zettel
       |text: Text of Zettel
       |bibkey: BibKey
       |bibtex: "@article{key, entries}"
       |""".stripMargin
    )

    val zettel =
      json
        .leftMap(err => err: Error)
        .flatMap(_.as[Zettel])
        .valueOr(throw _)

    zettel.title.get should be("My First Zettel")
    zettel.mentions.get should be(List("dbdennis", "gkt"))
    zettel.tags.get should be(List("Charles Babbage", "Ada Lovelace"))
    zettel.cite.get should be(Citation("Ifrah", Some(22), Some(36)))
    zettel.dates.get should be(Dates(1841, None, Some("CE")))
    zettel.summary.get should be("An amazing Zettel")
    zettel.text.get should be("Text of Zettel")
    zettel.bibkey.get should be("BibKey")
    zettel.bibtex.get should be("@article{key, entries}")
  }

  it should "be able to parse multi-YAML documents" in {
    val jsonStream = yaml.parser.parseDocuments(
      """
        |title: Zettel 1
        |---
        |title: Zettel 2
        |mentions:
        |- dbdennis
        |- gkt
        |tags:
        |- Charles Babbage
        |- Ada Lovelace
        |cite:
        |  bibkey: Ifrah
        |  page: 22
        |  last_page: 36
        |dates:
        |  year: 1841
        |  era: CE
        |summary: An amazing Zettel
        |text: Text of Zettel
        |bibkey: BibKey
        |bibtex: "@article{key, entries}"
        |""".stripMargin
    )

    val zStream = jsonStream map { json => json.leftMap(err => err: Error).flatMap(_.as[Zettel]).valueOr(throw _) }
    val zStreamIterator = zStream.iterator
    val first = zStreamIterator.next
    val second = zStreamIterator.next
    first.title.get should be("Zettel 1")
    second.title.get should be("Zettel 2")
  }

  it should "be able to load Zettels from files" in {

    val twoZettels = """
        |title: Zettel 1
        |---
        |title: Zettel 2
        |""".stripMargin

    info("creating scratch directory")
    val tmpDir = pwd / "scratch"
    mkdir ! tmpDir
    info("writing YAML to scratch directory")
    val yamlFile = pwd / "scratch" / "simple.yaml"
    if (exists ! yamlFile)
      rm ! yamlFile

    write(yamlFile, twoZettels)
    val jsonStream = yaml.parser.parseDocuments(new FileReader(yamlFile.toIO))
    val zStream = jsonStream map { json => json.leftMap(err => err: Error).flatMap(_.as[Zettel]).valueOr(throw _) }
    val zStreamIterator = zStream.iterator
    info("cleaning up scratch directory")
    rm ! yamlFile
  }

  it should "be able to parse a ZettelFass by splitting on --- and parsing each separately" in {
    val z1 = """
       |title: Zettel 1
       |""".stripMargin

    val z2 = """
       |title: Zettel 2
       |""".stripMargin

    val twoZettels = z1 + "---" + z2
    val twoZettelsSplit = twoZettels.split(raw"\-\-\-")

    twoZettelsSplit.length should be(2)
    twoZettelsSplit should be(Array(z1, z2))

    val jStream = twoZettelsSplit map { text => yaml.parser.parse(text) }

    val zStream = jStream.map { json => json.leftMap(err => err: Error).flatMap(_.as[Zettel]).valueOr(throw _) }
    val zStreamIterator = zStream.iterator
    val first = zStreamIterator.next
    val second = zStreamIterator.next
    first.title.get should be("Zettel 1")
    second.title.get should be("Zettel 2")
  }
}
