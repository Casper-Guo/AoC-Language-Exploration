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

def find_first_max(pack: String): (Char, Int) =
  // find the first occurence of the max battery in a pack
  pack.zipWithIndex.foldLeft(('0', 0)) {
    case ((current_max, max_index), (next_battery, next_index)) =>
      if next_battery > current_max
      then (next_battery, next_index)
      else (current_max, max_index)
  }

def part1(pack: String): Int =
  val (first_battery, first_index) = find_first_max(pack.dropRight(1))
  val (second_battery, _)          = find_first_max(pack.substring(first_index + 1))
  10 * first_battery.asDigit + second_battery.asDigit

def part2(pack: String): Long =
  val selected = (0 until 12).foldLeft((0, "")) {
    case ((start, on_batteries), num_on) =>
      val window_end               = pack.length - (12 - num_on)
      val window                   = pack.substring(start, window_end + 1)
      val (max_battery, max_index) = find_first_max(window)
      (start + max_index + 1, s"$on_batteries$max_battery")
  }
  selected(1).toLong

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input03.txt").getLines.toSeq
  println(input.map(part1).sum)
  println(input.map(part2).sum)
