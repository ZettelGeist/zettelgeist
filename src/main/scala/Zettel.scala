/*
 * Zettel.scala - an initial look at Zettels w/Scala case class and JSON format.
 *   This takes advantage of the json4s extract to case class capability. Very cool. 
 */

import org.json4s._
import org.json4s.jackson.JsonMethods._

/*
 * A Zettel is a note. All fields are either String or lists of Strings. We only use 
 * lists for fields where there is a clear need to separate the entries and be as flexible
 * as possible. tags, mentions, cite, and dates are likely the only cases (for now).
 */
 
case class Zettel( title: Option[String],
  tags: Option[List[String]],
  mentions: Option[List[String]],
  cite: Option[List[String]],
  dates: Option[List[String]],
  summary: Option[String],
  text: Option[String],
  bibkey: Option[String],
  bibtex: Option[String],
  ris: Option[String],
  inline: Option[String],
  note: Option[String],
  url: Option[String])

object SimpleZettelInJSON extends App {
  val zdoc = """{
    "title" : "My First Zettel",
    "mentions" : [ "dbdennis", "gkt"],
    "tags" : ["Charles Babbage", "Ada Lovelace"],
    "cite" : ["Ifrah", "22-36"],
    "dates" : [ "2000 CE", "1995-2000 CE"],
    "summary" : "An amazing Zettel",
    "text": "Text of Zettel",
    "bibkey" : "BibKey",
    "bibtex" : "@article{key, entries}"
  }
  """

  implicit val formats = DefaultFormats // Brings in default date formats etc.

  val json = parse(zdoc)
  val zettel = json.extract[Zettel]
  println(s"""title = ${zettel.title.getOrElse("")}""")
  println(s"""summary = ${zettel.summary.getOrElse("")}""")
  println(s"""text = ${zettel.text.getOrElse("")}""")
  println(s"""bibkey = ${zettel.bibkey.getOrElse("")}""")
  println(s"""bibtex = ${zettel.bibtex.getOrElse("")}""")
  println(s"""ris = ${zettel.ris.getOrElse("")}""")
  println(s"""inline = ${zettel.inline.getOrElse("")}""")
  println(s"""note = ${zettel.note.getOrElse("")}""")
  println(s"""url = ${zettel.url.getOrElse("")}""")
  println("tags = ")
  zettel.tags.getOrElse(List()) map { n => "\t" + n } foreach println
  zettel.mentions.getOrElse(List()) map { n => "\t" + n } foreach println
  zettel.cite.getOrElse(List()) map { n => "\t" + n } foreach println
}
