#!/usr/bin/env runhaskell
-- Usage:
--   ./a2.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Data.Char (isDigit)
import System.Environment (getArgs)

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  text
  & lines
  & map
    (\line ->
      let
        digits = filter isDigit line
        firstDigit = head digits
        lastDigit = last digits
      in
        read [firstDigit, lastDigit]
    )
  & sum
