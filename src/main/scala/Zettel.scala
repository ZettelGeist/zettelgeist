package zettelgeist

import java.io.File

case class Zettel(
  title: Option[String] = None,
  tags: Option[List[String]] = None,
  mentions: Option[List[String]] = None,
  cite: Option[Citation] = None,
  dates: Option[Dates] = None,
  summary: Option[String] = None,
  text: Option[String] = None,
  bibkey: Option[String] = None,
  bibtex: Option[String] = None,
  ris: Option[String] = None,
  inline: Option[String] = None,
  note: Option[String] = None,
  url: Option[String] = None
)

case class Dates(year: Int, last_year: Option[Int], era: Option[String])

case class Citation(bibkey: String, page: Option[Int], last_page: Option[Int])

object Zettel {
  def apply(file: File): Zettel = Zettel()
}
