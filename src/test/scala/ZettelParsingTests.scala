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
    zettel.dates.get should be (Dates(1841, None, Some("CE")))
  }

  it should "parse with no fields present in JSON zettel" in {
    val zettelInJson = "{}"

    implicit val formats = DefaultFormats // Brings in default date formats etc.

    val json = parse(zettelInJson)
    val zettel = json.extract[Zettel]

    zettel.title should be (None)
  }
}
