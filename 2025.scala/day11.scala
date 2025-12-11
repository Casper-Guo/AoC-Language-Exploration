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
//> using options -P:wartremover:traverser:org.wartremover.warts.While
//> using options -P:wartremover:traverser:org.wartremover.warts.Throw
//> using options -P:wartremover:traverser:org.wartremover.warts.Var

import scala.collection.mutable

def dfsSort(graph: Map[String, Set[String]]): List[String] =
  val visited     = mutable.Set[String]()
  val sortedNodes = mutable.ListBuffer[String]()

  def visit(node: String): Unit =
    if !visited(node) then
      visited += node
      graph.getOrElse(node, Set.empty).foreach(visit)
      sortedNodes.prepend(node)

  (graph.keySet ++ graph.values.flatten).foreach(visit)
  sortedNodes.toList

def countPaths(
    graph: Map[String, Set[String]],
    sortedNodes: List[String],
    startNode: String,
    endNode: String
): Long =
  val pathCounts = mutable.Map[String, Long]().withDefaultValue(0)
  pathCounts(startNode) = 1L

  for node <- sortedNodes do
    if pathCounts(node) > 0L then
      for neighbor <- graph.getOrElse(node, Set.empty) do
        pathCounts(neighbor) += pathCounts(node)

  pathCounts(endNode)

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input11.txt").getLines.map {
    case s"$from: $tos" =>
      val to_nodes = tos.split(" ").toSet
      from -> to_nodes
  }.toMap
  val sortedNodes = dfsSort(input)

  // part1
  println(countPaths(input, sortedNodes, "you", "out"))

  // part2
  val (seg1End, seg2End) =
    if sortedNodes.indexOf("fft") < sortedNodes.indexOf("dac")
    then ("fft", "dac")
    else ("dac", "fft")
  val seg1Paths = countPaths(input, sortedNodes, "svr", seg1End)
  val seg2Paths = countPaths(input, sortedNodes, seg1End, seg2End)
  val seg3Paths = countPaths(input, sortedNodes, seg2End, "out")
  println(seg1Paths * seg2Paths * seg3Paths)
