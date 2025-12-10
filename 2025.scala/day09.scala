//> using scala 3.7.4
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

type CoordL = (Long, Long)

def area(coord1: CoordL, coord2: CoordL): Long =
  val (x1, y1) = coord1
  val (x2, y2) = coord2
  (Math.abs(x1 - x2) + 1) * (Math.abs(y1 - y2) + 1)

def checkInteriorPoints(coord1: CoordL, coord2: CoordL, points: Seq[CoordL]): Boolean =
  val (x1, y1) = coord1
  val (x2, y2) = coord2
  val minx     = Math.min(x1, x2)
  val maxx     = Math.max(x1, x2)
  val miny     = Math.min(y1, y2)
  val maxy     = Math.max(y1, y2)

  points.exists {
    case (x, y) =>
      x > minx && x < maxx && y > miny && y < maxy
  }

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input09.txt").getLines.map {
    case s"$x,$y" => (x.toLong, y.toLong)
  }.toSeq
  // sort by area descending
  val rectAreas = input.zipWithIndex.combinations(2).map {
    case Seq((coord1, index1), (coord2, index2)) => (index1, index2, area(coord1, coord2))
  }.toSeq.sortBy(-_._3)
  println(rectAreas.headOption.getOrElse((0, 0, 0L))._3)

  // big indent in the input
  // 1916,50285
  // 94619,50285
  // 94619,48466
  // 1668,48466
  val part2Rect = rectAreas.find {
    (index1, index2, _) =>
      val (x1, y1)    = input(index1)
      val (x2, y2)    = input(index2)
      val aboveIndent = y1 >= 50285 && y2 >= 50285
      val belowIndent = y1 <= 48466 && y2 <= 48466
      (aboveIndent || belowIndent) && !checkInteriorPoints((x1, y1), (x2, y2), input)
  } match {
    case Some(sol) => sol
  }
  println(part2Rect)
