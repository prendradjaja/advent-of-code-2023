#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Data.List (isPrefixOf)
import System.Environment (getArgs)
import Control.Arrow ((>>>))

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  text
  & lines
  & map parseGame
  & map (\(gameId, observations) -> (gameId, foldr1 elementwiseMax observations))
  & filter (\(_, minPossible) -> allLTE minPossible myBag)
  & map fst
  & sum
  where
    myBag = (12, 13, 14)

parseGame game =
  (gameId, observations)
  where
    [gameId', observationsText] = split ": " game
    gameId = readInt (gameId' & words & last)
    observations =
      observationsText
      & split "; "
      & map parseObservation

parseObservation text =
  text
  & split ", "
  & map parseCubeCount
  & foldr1 elementwiseMax

parseCubeCount text =
  text
  & words
  & (\[n', color] -> (readInt n', color))
  & (\(n, color) ->
      case color of
        "red" -> (n, 0, 0)
        "green" -> (0, n, 0)
        "blue" -> (0, 0, n)
    )

elementwiseMax (r1, g1, b1) (r2, g2, b2) =
  (max r1 r2, max g1 g2, max b1 b2)

allLTE (r1, g1, b1) (r2, g2, b2) =
  all (== True) [r1 <= r2, g1 <= g2, b1 <= b2]

readInt = read :: String -> Int

split sep s = split' sep s [] ""
  where
    split' sep s parts curr
      | null s =
          parts ++ [curr]
      | sep `isPrefixOf` s =
          split'
            sep
            (drop (length sep) s)
            (parts ++ [curr])
            ""
      | otherwise =
          split'
            sep
            (tail s)
            parts
            (curr ++ [(head s)])
