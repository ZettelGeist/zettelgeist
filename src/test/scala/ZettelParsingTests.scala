/**
 * Created by gkt on 5/20/15.
 */

package zettelgeist

import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods._
import org.scalatest._

class ZettelParsingTests extends FlatSpec with Matchers {
  "Zettel" should "parse with all fields present in JSON zettel" in {
    val zettelInJSON = """{
      "title" : "My First Zettel",
      "mentions" : [ "dbdennis", "gkt"],
      "tags" : ["Charles Babbage", "Ada Lovelace"],
      "cite" : {
        "bibkey" : "Ifrah",
        "page": 22,
        "last_page": 36
      },
      "dates" : {
        "year" : 1841, "era" : "CE"
      },
      "summary" : "An amazing Zettel",
      "text": "Text of Zettel",
      "bibkey" : "BibKey",
      "bibtex" : "@article{key, entries}"
    }
    """
    implicit val formats = DefaultFormats // Brings in default date formats etc.

    val jsonAst = parse(zettelInJSON)
    val zettel = jsonAst.extract[Zettel]

    zettel.title.get should be ("My First Zettel")
    zettel.mentions.get should be (List("dbdennis","gkt"))
    zettel.tags.get should be (List("Charles Babbage", "Ada Lovelace"))
    zettel.cite.get should be (Citation("Ifrah", Some(22), Some(36)))
    zettel.dates.get should be (Dates(1841, None, Some("CE")))
    zettel.summary.get should be ("An amazing Zettel")
    zettel.text.get should be ("Text of Zettel")
    zettel.bibkey.get should be ("BibKey")
    zettel.bibtex.get should be ("@article{key, entries}")
  }

  it should "parse with no fields present in JSON zettel" in {
    val zettelInJson = "{}"

    implicit val formats = DefaultFormats // Brings in default date formats etc.

    val json = parse(zettelInJson)
    val zettel = json.extract[Zettel]

    zettel.title should be (None)
    zettel.mentions should be (None)
    zettel.tags should be (None)
    zettel.cite should be (None)
    zettel.dates should be (None)
    zettel.summary should be (None)
    zettel.text should be (None)
    zettel.bibkey should be (None)
    zettel.bibtex should be (None)
  }

  it should "parse with some fields present in JSON zettel" in {
    val zettelInJson = """{
      "title" : "My First Zettel",
      "mentions" : [ "dbdennis", "gkt"],
      "cite" : {
        "bibkey" : "Ifrah",
        "page": 22,
        "last_page": 36
      }
     }
    """

    implicit val formats = DefaultFormats // Brings in default date formats etc.

    val json = parse(zettelInJson)
    val zettel = json.extract[Zettel]

    zettel.title.get should be ("My First Zettel")
    zettel.mentions.get should be (List("dbdennis","gkt"))
    zettel.cite.get should be (Citation("Ifrah", Some(22), Some(36)))
    zettel.tags should be (None)
    zettel.dates should be (None)
    zettel.summary should be (None)
    zettel.text should be (None)
    zettel.bibkey should be (None)
    zettel.bibtex should be (None)
  }
}
