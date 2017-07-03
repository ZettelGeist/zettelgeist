package zettelgeist

import org.scalatest.FlatSpec
import org.scalatest._

/**
 * Created by gkt on 7/2/17.
 */

class ImportTests extends FlatSpec with Matchers {

  "Import" should "parse command line" in {
    import Import._

    val config = parseCommandLine(Array("--path", "../zettels", "--database", "zettels.db", "--validate"))

    config.get.database should be(Some("zettels.db"))
    config.get.dir should be(Some("../zettels"))
    config.get.validate should be(true)

  }

}
