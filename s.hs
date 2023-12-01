#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import System.Environment (getArgs)

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  text
