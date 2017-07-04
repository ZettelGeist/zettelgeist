package zettelgeist

import java.io.{ File, FileReader }

import cats.syntax.either._
import io.circe.{ Error, yaml }
import io.circe.generic.auto._
import io.circe.yaml
import scala.util._

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

object ZettelLoader {
  def apply(file: File): Stream[Zettel] = {
    val reader = new FileReader(file)
    println(s"Processing ${file.getName}")
    val jsonStream = yaml.parser.parseDocuments(reader)

    val result = Try {
      jsonStream map { json => json.leftMap(err => err: Error).flatMap(_.as[Zettel]).valueOr(throw _) }
    }
    result match {
      case Success(zettels) =>
        zettels
      case Failure(error) =>
        println(s"- ${file.getName}: ${error.getMessage}")
        Stream.empty[Zettel]
    }
  }
}
