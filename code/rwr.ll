
@c = global i32 0, align 4

; Function Attrs: nounwind uwtable
define i8* @writer(i8* %arg) #0 {
  %1 = alloca i8*, align 8
  store i8* %arg, i8** %1, align 8
  store volatile i32 2, i32* @c, align 4
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i8* @reader(i8* %arg) #0 {
  %1 = alloca i8*, align 8
  %local = alloca i32, align 4
  store i8* %arg, i8** %1, align 8
  %2 = load volatile i32, i32* @c, align 4
  store i32 %2, i32* %local, align 4
  ret i8* null
}
