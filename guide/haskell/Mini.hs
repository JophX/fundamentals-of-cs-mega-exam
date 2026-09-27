module Mini where

import Data.Char (isDigit, isSpace)

-- @block tokens
data Token = TNum Int | TPlus | TMinus | TTimes | TLParen | TRParen
  deriving Show

-- LEXER: characters -> tokens
lexer :: String -> [Token]
lexer [] = []
lexer (c:cs)
  | isSpace c = lexer cs                      -- skip whitespace
  | isDigit c = TNum (read (c : takeWhile isDigit cs))
                  : lexer (dropWhile isDigit cs)
  | c == '+'  = TPlus   : lexer cs
  | c == '-'  = TMinus  : lexer cs
  | c == '*'  = TTimes  : lexer cs
  | c == '('  = TLParen : lexer cs
  | c == ')'  = TRParen : lexer cs
  | otherwise = error ("lexical error: unexpected " ++ [c])
-- @end

-- @block ast
data Expr = Num Int | Add Expr Expr | Sub Expr Expr | Mul Expr Expr
  deriving Show
-- @end

-- @block parser
-- PARSER: tokens -> syntax tree.  Grammar (one function per rule):
--   expr   -> term   { ("+" | "-") term }      lowest precedence, left-assoc
--   term   -> factor { "*" factor }
--   factor -> NUMBER | "(" expr ")"            highest precedence
parse :: [Token] -> Expr
parse ts = case expr ts of
  (e, [])   -> e
  (_, rest) -> error ("syntax error at " ++ show rest)

expr :: [Token] -> (Expr, [Token])
expr ts = let (t, rest) = term ts in loop t rest
  where
    loop acc (TPlus  : r) = let (t, r') = term r in loop (Add acc t) r'
    loop acc (TMinus : r) = let (t, r') = term r in loop (Sub acc t) r'
    loop acc r            = (acc, r)

term :: [Token] -> (Expr, [Token])
term ts = let (f, rest) = factor ts in loop f rest
  where
    loop acc (TTimes : r) = let (f, r') = factor r in loop (Mul acc f) r'
    loop acc r            = (acc, r)

factor :: [Token] -> (Expr, [Token])
factor (TNum n : r)  = (Num n, r)
factor (TLParen : r) = case expr r of
  (e, TRParen : r') -> (e, r')
  _                 -> error "syntax error: expected )"
factor ts = error ("syntax error at " ++ show ts)
-- @end

-- @block eval
-- EXECUTOR: walk the tree
eval :: Expr -> Int
eval (Num n)   = n
eval (Add a b) = eval a + eval b
eval (Sub a b) = eval a - eval b
eval (Mul a b) = eval a * eval b

run :: String -> Int
run = eval . parse . lexer
-- @end
