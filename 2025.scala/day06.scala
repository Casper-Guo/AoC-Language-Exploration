//> using scala 3.7.4
//> using file utils.scala
//> using options -deprecation -feature -unchecked -Wunused:all
//> using plugin org.wartremover:::wartremover:3.4.1
//> using options -P:wartremover:traverser:org.wartremover.warts.Null
//> using options -P:wartremover:traverser:org.wartremover.warts.Return
//> using options -P:wartremover:traverser:org.wartremover.warts.AsInstanceOf
//> using options -P:wartremover:traverser:org.wartremover.warts.IsInstanceOf
//> using options -P:wartremover:traverser:org.wartremover.warts.StringPlusAny
//> using options -P:wartremover:traverser:org.wartremover.warts.OptionPartial
//> using options -P:wartremover:traverser:org.wartremover.warts.TryPartial
//> using options -P:wartremover:traverser:org.wartremover.warts.EitherProjectionPartial
//> using options -P:wartremover:traverser:org.wartremover.warts.IterableOps
//> using options -P:wartremover:traverser:org.wartremover.warts.Throw
//> using options -P:wartremover:traverser:org.wartremover.warts.Var
//> using options -P:wartremover:traverser:org.wartremover.warts.MutableDataStructures
//> using options -P:wartremover:traverser:org.wartremover.warts.While

def convertToCephalopod(textGrid: Grid[Char]): Grid[Long] =
  // numbers separated by commas, groups separated by tabs
  val alignedString = (0 until textGrid.numCols).map {
    col =>
      textGrid.getCol(col).mkString.trim match
        case ""  => "\t"
        case num => s"$num,"
  }.mkString
  Grid(alignedString.split("\t").map {
    group => group.split(",").map(_.toLong).toVector
  }.toVector)

@main def main(): Unit =
  val input     = scala.io.Source.fromFile("input06.txt").getLines.toSeq
  val operators = input.lastOption.getOrElse("").split(" +").toSeq
  val numberGrid = Grid(input.dropRight(1).map { row =>
    row.trim.split("\\s+").map(_.toLong).toVector
  }.toVector)
  val textGrid       = Grid(input.dropRight(1).map(row => row.toVector).toVector)
  val cephalopodGrid = convertToCephalopod(textGrid)

  val part1 = operators.zipWithIndex.map {
    case (op, index) =>
      op match
        case "*" => numberGrid.getCol(index).product
        case "+" => numberGrid.getCol(index).sum
  }.sum
  println(part1)

  val part2 = operators.zipWithIndex.map {
    case (op, index) =>
      op match
        case "*" => cephalopodGrid.getRow(index).product
        case "+" => cephalopodGrid.getRow(index).sum
  }.sum
  println(part2)
