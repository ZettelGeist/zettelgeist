/**
 * Created by gkt on 7/2/17.
 */

package zettelgeist

import scopt._
import java.io._

object Import {

  case class Config(database: Option[String] = None, dir: Option[String] = None, validate: Boolean = false)

  def parseCommandLine(args: Array[String]): Option[Config] = {
    val parser = new scopt.OptionParser[Config]("scopt") {
      head("ZettelGeist Import", "0.1.x")
      opt[String]('d', "database") action { (value, config) =>
        config.copy(database = Some(value))
      } text ("name of database (H2)")
      opt[String]('p', "path") action { (value, config) =>
        config.copy(database = Some(value))
      } text ("path to Zettel directory")
      opt[Unit]('v', "validate") action { (_, config) =>
        config.copy(validate = true)
      } text ("check validity of Zettels only (does not import into index)")
      help("help") text ("show help")
    }
    parser.parse(args, Config())
  }

  def go(config: Config): Unit = {
    val yamlFileStream = Utils.getFileTreeWithExtension(new File(config.dir.get), ".yaml")
  }

  def main(args: Array[String]) = {
    val config = parseCommandLine(args)
    println(config.get)
    go(config.get)
  }
}
