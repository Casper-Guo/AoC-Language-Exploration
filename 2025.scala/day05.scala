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

type Ranges = Seq[(Long, Long)]

def combine_ranges(ranges: Ranges): Ranges =
  val sortedRanges = ranges.sortBy(_._1)
  sortedRanges.foldLeft(Seq.empty[(Long, Long)]) { (acc, nextRange) =>
    val (nextStart, nextEnd) = nextRange
    acc.lastOption match {
      case Some((lastStart, lastEnd)) if nextStart <= lastEnd =>
        acc.dropRight(1) :+ (lastStart, Math.max(lastEnd, nextEnd))
      case _ =>
        acc :+ nextRange
    }
  }

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input05.txt").mkString.split("\n\n").toSeq
  val idRanges = input.headOption.getOrElse("").split('\n').map { line =>
    line match
      case s"$start-$end" => (start.toLong, end.toLong)
  }.toSeq
  val ids            = input.lastOption.getOrElse("").split('\n').map(_.toLong).toSeq
  val combinedRanges = combine_ranges(idRanges)
  // binary search is possible here but unnecessary for input size
  println(ids.count(id =>
    combinedRanges.exists { case (start, end) => id >= start && id <= end }
  ))
  println(combinedRanges.map { case (start, end) => end - start + 1 }.sum)
