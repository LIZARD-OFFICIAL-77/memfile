import sys
sys.path.append("..")

from memfile import memoryopen,remove

def test1():
    with memoryopen("testfile.txt","w") as file:
        file.write("Hello, world!")
    
    with memoryopen("testfile.txt") as file:
        assert file.read() == "Hello, world!",""
        
    with memoryopen("testfile.txt","w") as file:
        file.unlink()

def test2():
    with memoryopen("testfile2.bin","wb") as file:
        file.write(b"Hello, world!")
        
    with memoryopen("testfile2.bin","rb") as file:
        assert file.read() == b"Hello, world!"
        
    with memoryopen("testfile2.bin","w") as file:
        assert file.unlink()
        
passed = True

try:        
    test1()
    test2()
except Exception as e:
    print(f"ERROR: {e}")
    passed = False
finally:
    try:
        remove("testfile.txt")
    except:pass
    try:
        remove("testfile2.bin")
    except:pass
    
print(passed)