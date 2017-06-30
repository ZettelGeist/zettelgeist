package zettelgeist

case class Zettel(
  title: Option[String],
  tags: Option[List[String]],
  mentions: Option[List[String]],
  cite: Option[Citation],
  dates: Option[Dates],
  summary: Option[String],
  text: Option[String],
  bibkey: Option[String],
  bibtex: Option[String],
  ris: Option[String],
  inline: Option[String],
  note: Option[String],
  url: Option[String]
)

case class Dates(year: Int, last_year: Option[Int], era: Option[String])

case class Citation(bibkey: String, page: Option[Int], last_page: Option[Int])
