#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE

import Control.Arrow ((>>>))
import Data.Function ((&))
import System.Environment (getArgs)


main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text


pairwise xs =
  zip xs $ tail xs


diffs xs =
  xs
  & pairwise
  & map (uncurry $ flip (-))


extrapolate xs
  | all (== 0) xs =
    0
  | otherwise =
    let
      nextDiff = extrapolate $ diffs xs
    in
      last xs + nextDiff


solve text =
  text
  & lines
  & map (words >>> map readInt)
  & map extrapolate
  & sum


readInt = read :: String -> Int
