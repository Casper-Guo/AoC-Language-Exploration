//> using scala 3.7.4
//> using files utils.scala
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

def part1(grid: Grid[Char]): Int =
  val numSplits   = 0
  val initialRays = grid.getRow(0).map(_ == 'S')

  val (totalSplits, _) = (1 until grid.numRows).foldLeft((numSplits, initialRays)) {
    case ((currentSplits, currentRays), row) =>
      val currentRow = grid.getRow(row)
      val numSplit = currentRays.zipWithIndex.map {
        case (hasRay, col) =>
          if hasRay && currentRow(col) == '^' then 1 else 0
      }.sum
      val newRays = (0 until grid.numCols).map {
        col =>
          val straightDown = currentRays(col) && currentRow(col) != '^'
          val fromLeft     = col > 0 && currentRays(col - 1) && currentRow(col - 1) == '^'
          val fromRight =
            col < grid.numCols - 1 && currentRays(col + 1) && currentRow(col + 1) == '^'
          straightDown || fromLeft || fromRight
      }.toVector
      (currentSplits + numSplit, newRays)
  }
  totalSplits

def part2(grid: Grid[Char]): Long =
  val initialTimelines = grid.getRow(0).map {
    case 'S' => 1L
    case _   => 0L
  }

  val finalTimelines = (1 until grid.numRows).foldLeft(initialTimelines) {
    case (currentTimelines, row) =>
      val currentRow = grid.getRow(row)
      val newTimelines = (0 until grid.numCols).map {
        col =>
          val straightDown = if currentRow(col) != '^' then currentTimelines(col) else 0L
          val fromLeft =
            if col > 0 && currentRow(col - 1) == '^' then currentTimelines(col - 1) else 0L
          val fromRight = if col < grid.numCols - 1 && currentRow(col + 1) == '^' then
            currentTimelines(col + 1)
          else 0L
          straightDown + fromLeft + fromRight
      }
      newTimelines.toVector
  }
  finalTimelines.sum

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input07.txt").getLines
  val grid  = Grid(input.map(_.toVector).toVector)
  println(part1(grid))
  println(part2(grid))
