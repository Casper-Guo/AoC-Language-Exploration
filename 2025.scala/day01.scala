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

import java.lang.Math.floorMod

def part1(input: List[Int], start: Int = 50): Int =
  val (_, result) = input.foldLeft((start, 0)) {
    case ((current, count), instruction) =>
      val new_pos = floorMod(current + instruction, 100)
      (new_pos, if new_pos == 0 then count + 1 else count)
  }
  result

def part2(input: List[Int], start: Int = 50): Int =
  val (_, result) = input.foldLeft((start, 0)) {
    case ((current, count), instruction) =>
      val new_pos      = floorMod(current + instruction, 100)
      val current_zero = if new_pos == 0 then 1 else 0
      val traverse_zeros = instruction <= 0 match
        case true =>
          // new_pos > current implies at least one wrap around
          // except in the special case of starting at 0
          if new_pos > current && current != 0 then 1 + (instruction.abs / 100)
          else instruction.abs / 100
        case false =>
          // new_pos < current implies at least one wrap around
          // except in the special case of ending at 0
          if new_pos < current && new_pos != 0 then 1 + (instruction.abs / 100)
          else instruction.abs / 100

      // one last corner case of starting and ending on zero
      // in which we double count
      val total_zeros = if current == 0 && new_pos == 0 then
        current_zero + traverse_zeros - 1
      else
        current_zero + traverse_zeros
      (new_pos, count + total_zeros)
  }
  result

@main def day01(): Unit =
  val input = scala.io.Source.fromFile("input01.txt").getLines().toList.map {
    case s"R$rot" => rot.toInt
    case s"L$rot" => -rot.toInt
  }

  println(part1(input))
  println(part2(input))
