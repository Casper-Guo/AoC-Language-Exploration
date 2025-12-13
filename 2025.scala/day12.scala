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

def checkArea(presents: Seq[(Int, Seq[Seq[Int]])], region: (Int, Int, Seq[Int])): Boolean =
  val presentAreas = presents.map {
    case (_, present) => present.flatten.sum
  }.toSeq
  val (width, height, numPresents) = region
  val minArea = presentAreas.zip(numPresents).map {
    case (presentArea, numPresent) => presentArea * numPresent
  }.sum
  width * height >= minArea

def checkSquares(region: (Int, Int, Seq[Int])): Boolean =
  val (width, height, numPresents) = region
  (width / 3) * (height / 3) >= numPresents.sum

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input12.txt").mkString.split("\n\n").toSeq
  val presents = input.take(input.length - 1).map {
    case s =>
      val parts = s.split(":\n")
      val index = parts.headOption.getOrElse("0").toInt
      val grid = parts.lastOption.getOrElse("").split("\n").map {
        row => row.map(char => if char == '#' then 1 else 0).toSeq
      }.toSeq
      (index, grid)
  }.toSeq
  val regions = input.lastOption.getOrElse("").split("\n").map {
    case s"$dim: $presents" =>
      val (width, length) = (
        dim.split("x").headOption.getOrElse("0").toInt,
        dim.split("x").lastOption.getOrElse("0").toInt
      )
      (width, length, presents.split(" ").map(_.toInt).toSeq)
  }.toSeq
  println(regions.filter(checkArea(presents, _)).filter(checkSquares).size)
