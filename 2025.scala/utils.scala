type Coord = (Int, Int)
type Direction = (Int, Int)

class Grid[T](val grid: Vector[Vector[T]]) extends Iterable[T] {
  val numRows = grid.length
  val numCols = grid.headOption match {
    case None      => 0
    case Some(row) => row.length
  }

  // clockwise from north
  val neighborDelta = Vector((-1, 0), (0, 1), (1, 0), (0, -1))
  val adjDelta =
    Vector((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))

  def apply(row: Int): Vector[T] = grid(row)
  def apply(coord: Coord): T = grid(coord._1)(coord._2)

  override def equals(obj: Any): Boolean = obj match {
    case that: Grid[_] => this.grid == that.grid
    case _             => false
  }

  override def iterator: Iterator[T] =
    for {
      row <- (0 until numRows).iterator
      col <- (0 until numCols).iterator
    } yield apply((row, col))

  override def toString: String = grid.map(_.mkString(" ")).mkString("\n")

  def inBound(coord: Coord): Boolean = {
    val (row, col) = coord
    row >= 0 && row < numRows && col >= 0 && col < numCols
  }

  def euclid(coord1: Coord, coord2: Coord): Double = {
    val (row1, col1) = coord1
    val (row2, col2) = coord2
    Math.sqrt(Math.pow(row1 - row2, 2) + Math.pow(col1 - col2, 2))
  }

  def manhattan(coord1: Coord, coord2: Coord): Int = {
    val (row1, col1) = coord1
    val (row2, col2) = coord2
    Math.abs(row1 - row2) + Math.abs(col1 - col2)
  }

  def chebyshev(coord1: Coord, coord2: Coord): Int = {
    val (row1, col1) = coord1
    val (row2, col2) = coord2
    Math.max(Math.abs(row1 - row2), Math.abs(col1 - col2))
  }

  def coordsIter: Iterator[Coord] =
    for {
      row <- (0 until numRows).iterator
      col <- (0 until numCols).iterator
    } yield (row, col)

  def getRow(row: Int): Vector[T] = grid(row)

  def rowIter(row: Int): Iterator[(Coord, T)] =
    for {
      col <- (0 until numCols).iterator
    } yield ((row, col), grid(row)(col))

  def getCol(col: Int): Vector[T] = grid.map(row => row(col))

  def colIter(col: Int): Iterator[(Coord, T)] =
    for {
      row <- (0 until numRows).iterator
    } yield ((row, col), grid(row)(col))

  def at(coord: Coord): Option[T] =
    if (inBound(coord)) Some(apply(coord)) else None

  def directNeighborIter(coord: Coord): Iterator[(Coord, T)] =
    neighborDelta.iterator
      .map(delta => (coord._1 + delta._1, coord._2 + delta._2))
      .filter(inBound)
      .map(neighbor_coord => (neighbor_coord, apply(neighbor_coord)))

  def getDirectNeighbors(coord: Coord): Vector[T] =
    directNeighborIter(coord).map(_._2).toVector

  def adjNeighborIter(coord: Coord): Iterator[(Coord, T)] =
    adjDelta.iterator
      .map(delta => (coord._1 + delta._1, coord._2 + delta._2))
      .filter(inBound)
      .map(neighbor_coord => (neighbor_coord, apply(neighbor_coord)))

  def getAdjNeighbors(coord: Coord): Vector[T] =
    adjNeighborIter(coord).map(_._2).toVector

  def moveOne(coord: Coord, direction: Direction): Coord =
    (coord._1 + direction._1, coord._2 + direction._2)

  def moveN(coord: Coord, direction: Direction, n: Int): Coord =
    (coord._1 + direction._1 * n, coord._2 + direction._2 * n)

  def getDirection(from_coord: Coord, to_coord: Coord): Direction =
    (to_coord._1 - from_coord._1, to_coord._2 - from_coord._2)
}
