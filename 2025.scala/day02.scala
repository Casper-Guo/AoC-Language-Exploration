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

import scala.math.{ceil, floor, log10, max, min, pow}

def count_digits(num: Double): Int =
  ceil(log10(num)).toInt

def part1(interval: (Double, Double)): Double =
  val (start, end) = interval
  val start_digits = count_digits(start)
  val end_digits   = count_digits(end)

  (start_digits to end_digits)
    .filter(_ % 2 == 0) // odd digit numbers cannot have repeated halves
    .map { digits =>
      val digit_interval_start = max(start, pow(10, digits - 1))
      val digit_interval_end   = min(end, pow(10, digits) - 1)
      // a 6 digit number with repeated halves is divisible by 1001 etc.
      val divisor        = 1 + pow(10, digits / 2)
      val dividend_start = ceil(digit_interval_start / divisor)
      val dividend_end   = floor(digit_interval_end / divisor)
      (divisor * (dividend_start + dividend_end)) * (dividend_end - dividend_start + 1) / 2
    }
    .sum

def gen_divisors(num_digits: Double): Seq[Double] =
  (1 to num_digits.toInt / 2)
    .filter(num_digits % _ == 0)
    .map { repeated_seq_length =>
      // e.g. six digit number with repeated sequence length of 2
      // the first sequence is not shifted (10^0)
      // the second is shifted by two (10^2)
      // the third is shifted by four (10^4)
      // total divisor is 10^0 + 10^2 + 10^4
      (0 until num_digits.toInt by repeated_seq_length).map(pow(10, _)).sum
    }

def check_invalid(num: Long, divisors: Seq[Double]): Boolean =
  divisors.exists(divisor => num % divisor == 0)

def part2(inteval: (Double, Double)): Long =
  val (start, end) = inteval
  val start_digits = count_digits(start)
  val end_digits   = count_digits(end)
  val divisors     = (start_digits to end_digits).map(x => x -> gen_divisors(x)).toMap

  (start.toLong to end.toLong)
    .filter(x => check_invalid(x, divisors(count_digits(x.toDouble))))
    .sum

@main def main(): Unit =
  val input = scala.io.Source.fromFile("input02.txt").mkString.split(",").map {
    case s"$start-$end" => (start.toDouble, end.toDouble)
  }.toSeq
  println(input.map(part1).sum.toLong)
  println(input.map(part2).sum)
