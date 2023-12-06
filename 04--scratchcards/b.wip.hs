#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import System.Environment (getArgs)
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Map ((!))


-- WIP: All the parts are implemented, but there's a bug somewhere (wrong
-- answer)
--
-- Use b.verbose.py as a debugging aid
main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text


solve text =
  sum finalCardCounts
  where
    matchCounts =
      text
      & lines
      & map getMatches

    lastCardNumber = length matchCounts

    initialCardCounts =
      zip [1..lastCardNumber] (repeat 1)
      & Map.fromList

    finalCardCounts =
      foldl
        (\accCardCounts (i, currMatchCount) ->
          let
            nextIndex = i + 1
            toCopy = -- List of card numbers to make copies of (possibly empty)
              [nextIndex .. (nextIndex + currMatchCount - 1)]
          in
            copyCards currMatchCount toCopy accCardCounts
        )
        initialCardCounts
        (zip [1..] matchCounts)


-- Make N copies of KEYS_TO_COPY in CARD_COUNTS
copyCards n keysToCopy cardCounts =
  foldl
    (\accCardCounts currKey ->
      let
        oldValue = accCardCounts ! currKey
        newValue = oldValue + n
      in
        Map.insert currKey newValue accCardCounts
    )
    cardCounts
    keysToCopy


-- Parse a card and count matches
getMatches card =
  card

  -- Take only after the ':'
  & dropWhile (/= ':')
  & drop 1

  -- Split on '|' and parse ints
  & map (\c -> if c == '|' then '\n' else c)
  & lines
  & map readIntsToSets

  -- Count matches
  & \[winners, chosen] -> Set.intersection winners chosen
  & Set.size


-- e.g. readIntsToSets "1 2 3" == Set.fromList [1, 2, 3]
readIntsToSets s =
  s
  & words
  & map readInt
  & Set.fromList


readInt = read :: String -> Int
