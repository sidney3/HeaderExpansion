# HeaderExpansion

`HeaderExpansion` is a tool that expands header files from a given template directory.

Given a directory `template_directory` and some file `run.cpp`, with `run.cpp` referencing files in `template_directory` via its `#include` statements, running

```
Python3 <path to HeaderExpansion/src/main.py> <path to template_directory> <path to run.cpp>
```

Will expand any of these include statements recursively. This allows you to build a library of template components, with nested dependencies, and access them quickly for competitive programming.

## Why use the tool?

Why use this tool over a large snippets library? This allows you to nest dependencies (i.e. have one template component that includes another) without having to copy paste the required module. Moreover, if you want to write tests for your template library, as you should, this is difficult if you are using snippets. This tool allows you to write comprehensive competitive programming libraries like a __Software Engineer__.

## Suggested Use

As the location of this directory and the location of your template directory will be static, this tool is intended to be used with the following style of command mapping.

```
ExpandDependencies = function()
    BUILD_PATH = <path to this cloned directory>/src/main.py
    TEMPLATE_PATH = <path to your template library>
    vim.cmd("!Python3 " .. BUILD_PATH .. " " .. TEMPLATE_PATH .. " $PWD/%") 
end

vim.api.nvim_create_user_command('B', ExpandDependencies, {}) -- build
```

## Example Usage

Consider the following template structure:

```
-- Templates
|
|
|---Math
    |
    |-GetPrimes.cpp
    |-GetPrimeFactorization.cpp
```

Where `GetPrimes.cpp` is a dependency of `GetPrimeFactorization.cpp`. Then, to quickly build up the prime factorization, rather than worrying about importing both `GetPrimes.cpp` and `GetPrimeFactorization.cpp`, a program like follows would suffice (assuming `GetPrimeFactorization.cpp` has a function member `PF`)

```
// run.cpp

#include <Math/GetPrimeFactorization.cpp>
#include <iostream>
#include <unordered_map>

int main()
{
    int target;
    std::cin >> target;
    std::unordered_map<int, int> primeFactorization = PF(target);
    for(auto [prime, count] : primeFactorization)
    {
        std::cout << prime << ", " << count << "\n";
    }

}
```

And running `:B` (or whatever you map the build script to), would expand `#include <Math/GetPrimeFactorization.cpp>` into the raw definitions of these two files, while merging and pulling all STL includes to the top of the file.

