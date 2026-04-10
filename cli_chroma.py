import chromadb

def vd(num=0):
    id = f'{file}_{num:03d}'
    print(f'{id}:')
    print(col.get(ids=[id])['documents'][0])
    
file='vbs.md'
print(f'file: {file}')

client = chromadb.PersistentClient(path="chroma")
cols = client.list_collections()
for i, col in enumerate(cols):
    print(f'{i}: {col.name}: {col.metadata}')
col = cols[0]
print(f'col=0: {col.name} (col=col[<num>])')
breakpoint()
