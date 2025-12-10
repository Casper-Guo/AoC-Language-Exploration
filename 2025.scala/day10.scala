//> using scala 3.7.4
//> using options -deprecation -feature -unchecked -Wunused:all
//> using plugin org.wartremover:::wartremover:3.4.1
//> using options -P:wartremover:traverser:org.wartremover.warts.Null
//> using options -P:wartremover:traverser:org.wartremover.warts.AsInstanceOf
//> using options -P:wartremover:traverser:org.wartremover.warts.IsInstanceOf
//> using options -P:wartremover:traverser:org.wartremover.warts.StringPlusAny
//> using options -P:wartremover:traverser:org.wartremover.warts.OptionPartial
//> using options -P:wartremover:traverser:org.wartremover.warts.TryPartial
//> using options -P:wartremover:traverser:org.wartremover.warts.EitherProjectionPartial
//> using options -P:wartremover:traverser:org.wartremover.warts.IterableOps
//> using options -P:wartremover:traverser:org.wartremover.warts.Throw
//> using options -P:wartremover:traverser:org.wartremover.warts.Var

import scala.collection.mutable.{ArrayDeque, Set}

def part1(program: Int, schema: Seq[Int], start: Int = 0): Int =
  val queue   = ArrayDeque[(Int, Int)]((start, 0))
  val visited = Set[Int](start)

  while queue.nonEmpty do
    val (state, steps) =
      queue.removeHeadOption() match { case Some((state, steps)) => (state, steps) }
    if state == program then
      return steps
    schema.map(_ ^ state).filter(!visited.contains(_)).foreach { nextState =>
      visited.add(nextState)
      queue.append((nextState, steps + 1))
    }

  -1

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input10.txt").getLines.map {
    case s"[$program] $schemas {$joltages}" => (program, schemas, joltages)
  }.toSeq
  val programs = input.map(_._1).map {
    _.zipWithIndex.map {
      case (light, index) => (if light == '#' then 1 else 0) << index
    }.sum
  }
  val schemas = input.map(_._2).map {
    _.split(" ").map { case s"($lights)" => lights.split(",").map(1 << _.toInt).sum }.toSeq
  }
  // val joltages = input.map(_._3).map(_.split(",").map(_.toInt).toSeq)

  println(programs.zip(schemas).map { case (program, schema) => part1(program, schema) }.sum)
