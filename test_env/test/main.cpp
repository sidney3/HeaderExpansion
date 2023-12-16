#include <unrelated>
#include <sub_dir/sub_sub_dir/dependency2.cpp>
#include <sub_dir/dependency1.cpp>

int main()
{
    for(int i = 0; i < 6; i++)
    {
        cout << "This is a file that does things\n";
    }
}
