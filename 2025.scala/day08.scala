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
//> using options -P:wartremover:traverser:org.wartremover.warts.While

import scala.collection.mutable

type JBox = (Int, Int, Int)

def dist(box1: JBox, box2: JBox): Double =
  val (x1, y1, z1) = box1
  val (x2, y2, z2) = box2
  Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2) + Math.pow(z1 - z2, 2)

def find(box: JBox, parents: mutable.Map[JBox, JBox]): JBox =
  if parents(box) == box then box
  else
    parents(box) = find(parents(box), parents)
    parents(box)

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input08.txt").getLines.map {
    _ match { case s"$x,$y,$z" => (x.toInt, y.toInt, z.toInt) }
  }.toSeq

  val maxConnects      = 1000
  val nLargestCircuits = 3
  val dists =
    input.combinations(2).map { case Seq(box1, box2) => (box1, box2, dist(box1, box2)) }.toSeq
      .sortBy(_._3)

  // part 1
  var parents        = mutable.Map(input.map(box => box -> box)*)
  var sizes          = mutable.Map(input.map(box => box -> 1L)*)
  var lastConnection = ((0, 0, 0), (0, 0, 0))

  // connect
  for ((box1, box2, _) <- dists.take(maxConnects)) {
    val root1 = find(box1, parents)
    val root2 = find(box2, parents)

    if root1 != root2 then {
      val size1 = sizes(root1)
      val size2 = sizes(root2)

      if size1 < size2 then {
        parents(root1) = root2
        sizes(root2)   = size1 + size2
      } else {
        parents(root2) = root1
        sizes(root1)   = size1 + size2
      }
    }
    lastConnection = (box1, box2)
  }

  // sort circuit sizes descending
  var circuitSizes =
    input.map(box => find(box, parents)).distinct.map(root => sizes(root)).toSeq.sortBy(-_)
  println(circuitSizes.take(nLargestCircuits).map(_.toLong).product)

  // part 2
  for ((box1, box2, _) <- dists.takeRight(dists.length - maxConnects)) {
    val root1 = find(box1, parents)
    val root2 = find(box2, parents)

    if root1 != root2 then {
      val size1 = sizes(root1)
      val size2 = sizes(root2)

      if size1 < size2 then {
        parents(root1) = root2
        sizes(root2)   = size1 + size2
      } else {
        parents(root2) = root1
        sizes(root1)   = size1 + size2
      }
      lastConnection = (box1, box2)
    }
  }

  var (lastBox1, lastBox2) = lastConnection
  println(lastBox1._1.toLong * lastBox2._1.toLong)
