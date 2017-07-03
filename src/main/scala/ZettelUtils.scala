package zettelgeist

import scala.collection.JavaConversions._
import java.io._

object Utils {

  // Inspired by https://stackoverflow.com/questions/14526260/how-do-i-get-the-file-name-from-a-string-containing-the-absolute-file-path
  def getFileTree(f: File): Stream[File] =
    f #:: (if (f.isDirectory) f.listFiles().toStream.flatMap(getFileTree)
    else Stream.empty)

  // Support filtering by extension via composition
  def getFileTreeWithExtension(f: File, extension: String = ".yaml"): Stream[File] =
    getFileTree(f).filter(_.getName().endsWith(".yaml"))
}
