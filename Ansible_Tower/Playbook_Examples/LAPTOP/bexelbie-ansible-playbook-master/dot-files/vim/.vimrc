" PUBLIC FILE
"
" Plugin Management via Vundle
" https://github.com/gmarik/Vundle.vim
" Installation:
" 1. git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
" 2. Launch vim and run :PluginInstall or to install from command line: vim +PluginInstall +qall
"-------------------------------------------------------------------------------
" Vundle Setup
"-------------------------------------------------------------------------------
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
" call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

" diff marks in files - https://github.com/airblade/vim-gitgutter
Plugin 'airblade/vim-gitgutter'

" https://github.com/bling/vim-airline
Plugin 'bling/vim-airline'

" git@github.com:bexelbie/vim-reveal.git
" use index.html for output filename
" save the presentation in $CWD
" put reveal one level down
" Set root_path to $CWD
let g:reveal_config = {
                      \'filename': 'index',
                      \'outputPathDirname': '',
                      \'revealWebPath': '..\/tools\/reveal.js\/',
                      \'dependencies': '..\/tools\/reveal.js\/plugin\/menu\/menu.js',
                      \'path': ''}
Plugin 'bexelbie/vim-reveal'

"https://github.com/vim-syntastic/syntastic
Plugin 'vim-syntastic/syntastic'

" set default location
let g:vimwiki_list = [{'path': '~/.vimwiki/'}]

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

"-------------------------------------------------------------------------------
" Other
"-------------------------------------------------------------------------------

"fix tabs
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab

" Set folding
set foldmethod=marker

" Turn on syntax highlighting, or really color coding.
syntax on

" Spelling
set spelllang=en_us
" toggle spellcheck
set <F8>=[19~
nmap <silent> <F8> :set spell!<CR>

" Highlight all matches on a search
" Disable with :set nohlsearch
" Use * to search for current position word
:set hlsearch

map N :n
map ** !}fmt
map *4 !}fmt -w 40
map *6 !}fmt -w 60
map *t !}fmt -t
map *c !}fmt -c

" Display a status-bar.
set laststatus=2

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Here begins my automated wordcount addition.
" This combines several ideas from:
" http://stackoverflow.com/questions/114431/fast-word-count-function-in-vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:word_count="<unknown>"
function WordCount()
  return g:word_count
endfunction
function UpdateWordCount()
  let lnum = 1
  let n = 0
  while lnum <= line('$')
    let n = n + len(split(getline(lnum)))
    let lnum = lnum + 1
  endwhile
  let g:word_count = n
endfunction
" Update the count when cursor is idle in command or insert mode.
" Update when idle for 1000 msec (default is 4000 msec).
set updatetime=500
augroup WordCounter
  au! CursorHold,CursorHoldI * call UpdateWordCount()
augroup END
set statusline=%{WordCount()}\ words
" Set statusline, shown here a piece at a time
"highlight User1 ctermbg=green guibg=green ctermfg=black guifg=black
"set statusline=%1*			" Switch to User1 color highlight
"set statusline+=%<%F		" file name, cut if needed at start
"set statusline+=%M			" modified flag
"set statusline+=%y			" file type
"set statusline+=%=			" separator from left to right justified
"set statusline+=\ %{WordCount()}\ words,
"set statusline+=\ %l/%L\ lines,\ %P	" percentage through the file

"syntastic
"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*
"
"let g:syntastic_always_populate_loc_list = 1
"let g:syntastic_auto_loc_list = 1
"let g:syntastic_check_on_open = 1
"let g:syntastic_check_on_wq = 0
"let g:syntastic_enable_proselint=1
"let g:syntastic_markdown_checkers = ["proselint"]
