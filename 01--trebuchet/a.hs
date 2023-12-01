#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE

import Data.Char (isDigit)
import System.Environment (getArgs)

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  sum $ map getCalibrationValue (lines text)

getCalibrationValue line =
  read [firstDigit, lastDigit]
  where
    digits = filter isDigit line
    firstDigit = head digits
    lastDigit = last digits
