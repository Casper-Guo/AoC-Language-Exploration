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

import scala.annotation.tailrec

def part1(grid: Grid[Char], coord: Coord): Boolean =
  if grid(coord) != '@' then false
  else
    grid.getAdjNeighbors(coord).filter(_ == '@').length < 4

@tailrec
def removePaper(grid: Grid[Char]): Grid[Char] =
  val new_grid = Grid(
    (0 until grid.numRows).map {
      row =>
        grid.rowIter(row).map {
          case (coord, value) =>
            if part1(grid, coord) then '.' else value
        }.toVector
    }.toVector
  )
  if new_grid == grid then new_grid else removePaper(new_grid)

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input04.txt").getLines.map(_.toVector).toVector
  val grid  = Grid(input)
  val initialPaperCount = grid.filter(_ == '@').size
  println(grid.coordsIter.filter(coord => part1(grid, coord)).length)

  val finalPaperCount = removePaper(grid).filter(_ == '@').size
  println(initialPaperCount - finalPaperCount)
