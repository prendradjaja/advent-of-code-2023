#!/usr/bin/env runhaskell
-- Usage:
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Char (isDigit)
import Data.Function ((&))
import Data.List (isPrefixOf)
import Data.Maybe (mapMaybe)
import System.Environment (getArgs)

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  sum $ map getCalibrationValue (lines text)

getCalibrationValue line =
  firstDigit * 10 + lastDigit
  where
    digits = getDigits line
    firstDigit = head digits
    lastDigit = last digits

getDigits s = mapMaybe getDigit $ suffixes s

-- Given a string s, return e.g.
--   Just 1 if it starts with "1" or "one"
--   Just 2 if it starts with "2" or "two"
--   ...
--   Nothing otherwise
--
-- Examples:
--   getDigit "onetwothree" = Just 1
--   getDigit "1twothree" = Just 1
--   getDigit "other1twothree" = Nothing
getDigit s
  | isPrefixOf "1" s = Just 1
  | isPrefixOf "2" s = Just 2
  | isPrefixOf "3" s = Just 3
  | isPrefixOf "4" s = Just 4
  | isPrefixOf "5" s = Just 5
  | isPrefixOf "6" s = Just 6
  | isPrefixOf "7" s = Just 7
  | isPrefixOf "8" s = Just 8
  | isPrefixOf "9" s = Just 9
  | isPrefixOf "one" s = Just 1
  | isPrefixOf "two" s = Just 2
  | isPrefixOf "three" s = Just 3
  | isPrefixOf "four" s = Just 4
  | isPrefixOf "five" s = Just 5
  | isPrefixOf "six" s = Just 6
  | isPrefixOf "seven" s = Just 7
  | isPrefixOf "eight" s = Just 8
  | isPrefixOf "nine" s = Just 9
  | otherwise = Nothing

suffixes [] = []
suffixes s@(_:xs) =
  s : (suffixes xs)
